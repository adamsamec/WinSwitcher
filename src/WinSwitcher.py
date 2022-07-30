from pathlib import Path
import rich
import subprocess
import sys
from threading import Thread
import win32api
import win32gui
import win32process

import psutil
from pynput import keyboard
from pywinauto import Application
import wx

from config import Config
from gui import MainFrame
from lang import _

# Exception used when filtering apps.
class SkipApp(Exception):
  pass

# Main application class.
class WinSwitcher:

  # App names and window process filenames which to exclude from the list
  EXCLUDED_APP_NAMES = ['ApplicationFrameHost', 'SystemSettings', 'TextInputHost']
  EXCLUDED_WINDOW_FILENAMES = ['ApplicationFrameHost.exe', 'SystemSettings.exe', 'TextInputHost.exe']

  # Replacements for app titles to make them shorter or more readable
  REPLACED_APP_TITLES = {
    'Windows Explorer': _('File Explorer'),
    'Windows Command Processor': _('Command Prompt'),
  }

  # Initializes the object.
  def __init__(self, config):
    self.config = config  
    self.pressedKeys = set()
    self.pid= self.getForegroundAppPid()
    self.prevAppPid = self.pid
    self.runningWindows = []

  # Returns the PID of the window in the foreground.
  def getForegroundAppPid(self):
    pids = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return pids[-1]

      # Sets the apps UI object for the switcher and saves its process PID.
  def setUI(self, ui):
    self.ui = ui
    hwnd = ui.GetHandle()
    self.guiPid = win32process.GetWindowThreadProcessId(hwnd)[1]

  # Returns the info about the app specified by the given PID.
  def getAppInfo(self, pid):
    process = psutil.Process(pid)
    path = process.exe()
    filename = Path(path).name
    langs = win32api.GetFileVersionInfo(path, r'\VarFileInfo\Translation')
    key = r'StringFileInfo\%04x%04x\FileDescription' % (langs[0][0], langs[0][1])
    title = (win32api.GetFileVersionInfo(path, key))
    if title in list(WinSwitcher.REPLACED_APP_TITLES.keys()):
      title = WinSwitcher.REPLACED_APP_TITLES[title]
    info= {
      'pid': pid,
      'filename': filename,
      'path': path,
      'title': title,
    }
    return info

  # Handler which is called for each running window and saves its information.
  def winEnumHandler(self, hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
      title = win32gui.GetWindowText(hwnd)
      if not title:
        return
      threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
      filename = psutil.Process(processId).name()
      if filename in WinSwitcher.EXCLUDED_WINDOW_FILENAMES:
        return
      window = {
        'threadId': threadId,
        'processId': processId,
        'hwnd': hwnd,
        'filename': filename,
        'title': title,
      }
      self.runningWindows.append(window)

  # Updates the list of the currently running windows.
  def updateRunningWindows(self):
    self.runningWindows = []
    win32gui.EnumWindows(self.winEnumHandler, None)

    # Rename the  title for File Explorer desktop item
    window = self.runningWindows[-1]
    if (window['filename'] == 'explorer.exe') and (window['title'] == 'Program Manager'):
      window['title'] = _('Program Manager')

  # Returns a list of running apps where each app consists of info about itss PID, process filename, app title and its running windows.
  def getRunningAppsAndWindows(self):
    gpCommand = 'powershell "Get-Process | where {$_.MainWindowTitle } | select ProcessName, Id | Format-List"'
    gpProcess = subprocess.Popen(gpCommand, shell=True, stdout=subprocess.PIPE)
    
      # decode() converts from binary string and rstrip() removes trailing "\r\n"
    lines = [line.decode().rstrip() for line in gpProcess.stdout if not line.decode()[0].isspace()]

    lineCount = len(lines)
    lineNum = 0
    propCount = 2
    apps = []
    while lineNum < lineCount:
      line = lines[lineNum]
      modLineNum = lineNum % propCount
      value = line[line.find(':') + 2:]

      # Process name
      if modLineNum == 0:
        skipApp = False
        name = value

        # Skip some strange unwanted apps
        if name in WinSwitcher.EXCLUDED_APP_NAMES:
          skipApp =True

      # PID
      elif (modLineNum == 1) and not skipApp:
        pid = int(value)
        app = self.getAppInfo(pid)
        app['name'] = name
        apps.append(app)
      lineNum += 1

    # File Explorer is not listed, so add it separately
    explorerFilename = 'explorer.exe'
    tasklistCommand = f'tasklist /FI "ImageName eq {explorerFilename}" /FI "Status eq Running" /FO LIST'
    tasklistProcess = subprocess.Popen(tasklistCommand, shell=True, stdout=subprocess.PIPE)

    # PID line is the third one
    pidLine = tasklistProcess.stdout.readlines()[2].decode()

    pid = int(pidLine.split()[-1])
    app = self.getAppInfo(pid)
    app['name'] = 'FileExplorer'
    apps.insert(0, app)

    # Complete the apps dictionary with the corresponding running windows and group the apps based on process path
    self.updateRunningWindows()
    groupIndexes = {}
    groupedApps = []
    for index, app in enumerate(apps):
      groupName = app['path']
      app['windows'] = []
      skipApp = False
      for window in self.runningWindows:
        if window['processId'] == app['pid']:
          try:
            groupIndexes[groupName]

            # We are on an app for which we've already created a group, so add its window to the app at the saved index

            # If app's windows are empty, we have already added them to the group instead, so skip this app addition to the grouped apps
            if len(app['windows']) == 0:
              skipApp = True

          except KeyError:
            # We are on  an app for which we've not yet created a group, so create the group and save the app'ss index to it
            groupIndexes[groupName] = index
            # app['windows'].append(window)

          if window['filename'] == explorerFilename:
            # Add hwnd for the FileExplorer app if not already added
            try:
              app['lastWindowHwnd']
            except KeyError:
              app['lastWindowHwnd'] = window['hwnd']
          apps[groupIndexes[groupName]]['windows'].append(window)
      if not skipApp:
        groupedApps.append(app)
    apps = groupedApps

    # Add window count to the app title
    for app in apps:
      count = len(app['windows'])
      if app['filename'] == explorerFilename:
        # Do not count Desktop as a window of File Explorer
        count -= 1
      countText = _('{} windows').format(count)
      app['title'] += f' ({countText})'
    # rich.print(apps)
    return apps

  # Returns a list of running windows for the application with the given PID.
  def getAppWindows(self, pid):
    self.updateRunningWindows()
    windows = []
    for window in self.runningWindows:
      if window['processId'] == pid:
        windows.append(window)
    return windows

  # Switches to the given app.
  def switchToApp(self, app):
    pid = app['pid']
    try:
      # Apps which cannot be switched via PID are switched via hwnd of their last window
      app['lastWindowHwnd']
    except KeyError:
      try:
        app = Application().connect(process=pid)
        app.top_window().set_focus()
      except:
        print(f'Switching to app with PID: {pid} failed.')
      return
    self.switchToWindow(app['lastWindowHwnd'])

  # Switches to the window specified by the given hwnd.
  def switchToWindow(self, hwnd):
    try:
      win32gui.SetForegroundWindow(hwnd)
    except:
      print(f'Switching to window with handle: {hwnd} failed.')

  # Shows the app switcher.
  def showSwitcher(self, type, args):
    foregroundAppPid = self.getForegroundAppPid()
    if foregroundAppPid != self.guiPid:
      self.prevAppPid = foregroundAppPid
    isStayingInSwitcher = foregroundAppPid == self.guiPid
    # self.hideSwitcher()
    if type == 'apps':
      apps = self.getRunningAppsAndWindows()
      self.ui.updateListUsingApps(apps)
    elif type == 'windows':
      pid = self.getForegroundAppPid() if not isStayingInSwitcher else self.prevAppPid
      windows = self.getAppWindows(pid)
      self.ui.updateListUsingForegroundAppWindows(windows)
    if isStayingInSwitcher:
      return
    self.ui.show()
    # self.ui.Iconize(False)
    app = {'pid': self.pid}
    self.switchToApp(app)
    self.ui.Raise()

  # Hides the app switcher and switches to the window which was previously in the foreground.
  def hideSwitcherAndShowPrevWindow(self):
    self.hideSwitcher()
    app = {'pid': self.prevAppPid}
    self.switchToApp(app)

  # Hides the app switcher.
  def hideSwitcher(self):
    self.ui.hide()

  # Called when switched out of the apps window.
  def windowDeactivated(self):
    self.hideSwitcher()

  # Exits the program.
  def exitSwitcher(self):
    self.ui.cleanAndClose()
    sys.exit()

  # Called when key is pressed.
  def onKeyDown(self, key):
    self.pressedKeys.add(key)

  # Called when key is released.
  def onKeyUp(self, key):
    # print(self.pressedKeys)
    shortcuts = self.config.getShortcuts()
    for shortcut in shortcuts:
      for keys in shortcut['keys']:
        if keys.issubset(self.pressedKeys):
          command = shortcut['command']
          if command == 'showApps':
            # running showSwitcher() in a new thread fixes the issue of Win key not being released after calling showSwitcher()
            thread = Thread(target=self.showSwitcher, args=('apps', None))
            thread.start()
          if command == 'showWindows':
            thread = Thread(target=self.showSwitcher, args=('windows', None))
            thread.start()
          elif command == 'exit':
            self.exitSwitcher()

    if key in self.pressedKeys:
      self.pressedKeys.remove(key)

# Main function.
def main():
  app = wx.App()
  config = Config()
  switcher = WinSwitcher(config)
  mainFrame = MainFrame(switcher, config, title=MainFrame.WINDOW_TITLE)
  switcher.setUI(mainFrame)
  with keyboard.Listener(on_press=switcher.onKeyDown, on_release=switcher.onKeyUp) as listener:
    app.MainLoop()
    listener.join()
    del app

main()
