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

# Main application class.
class WinSwitcher:

  # Process names which to exclude from the apps and windows list
  EXCLUDED_APPS = ['ApplicationFrameHost', 'SystemSettings', 'TextInputHost']
  EXCLUDED_WINDOWS = ['ApplicationFrameHost.exe', 'SystemSettings.exe', 'TextInputHost.exe']

  # Initializes the object.
  def __init__(self, config):
    self.config = config  
    self.pressedKeys = set()
    self.appsWindowPid= self.getForegroundWindowPid()
    self.prevWindowPid = self.appsWindowPid
    self.runningWindows = []

  # Returns the PID of the window in the foreground.
  def getForegroundWindowPid(self):
    pids = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return pids[-1]

      # Sets the apps UI object for the switcher.
  def setAppsAppsUI(self, ui):
    self.appsUi = ui

  # Returns the title of the app specified by PID
  def getAppTitle(self, pid):
    process = psutil.Process(pid)
    path = process.exe()
    langs = win32api.GetFileVersionInfo(path, r'\VarFileInfo\Translation')
    key = r'StringFileInfo\%04x%04x\FileDescription' % (langs[0][0], langs[0][1])
    title = (win32api.GetFileVersionInfo(path, key))
    return title

  # Handler which is called for each running window and saves its information.
  def winEnumHandler(self, hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
      title = win32gui.GetWindowText(hwnd)
      if not title:
        return
      childPid, parentPid = win32process.GetWindowThreadProcessId(hwnd)
      # childPid = pids[0]
      # parentPid = pids[1]
      exe = psutil.Process(parentPid).name()
      if exe in WinSwitcher.EXCLUDED_WINDOWS:
        return
      window = {
        'childPid': childPid,
        'parentPid': parentPid,
        'title': title,
      }
      self.runningWindows.append(window)

  # Returns the list of running apps titles, their PIDs and corresponding windows.
  def getRunningAppsAndWindows(self):
    gpsCommand = 'powershell "Get-Process | where {$_.MainWindowTitle } | select ProcessName,Id"'
    gpsProcess = subprocess.Popen(gpsCommand, shell=True, stdout=subprocess.PIPE)
    apps = []
    i = 0
    for line in gpsProcess.stdout:
      if (i > 2) and (not line.decode()[0].isspace()):
        # Skip the first two lines (the header)
        # Only get lines that are not empty
        # decode() is necessary to get rid of the binary string (b')
        # rstrip() to remove `\r\n`
        line = line.decode().rstrip()
        parts = line.split()
        pid = parts[-1]

        # Skip some strange application items
        name = line[:-len(pid)].rstrip()
        if name in WinSwitcher.EXCLUDED_APPS:
          continue

        pidNum = int(pid)
        title = self.getAppTitle(pidNum)
        app = {
          'pid': pidNum,
          'title': title,
        'windows': []
        }
        apps.append(app)
        print(f'{name} {pid} {title}')
      i = i + 1

    # File Explorer is not listed, so handle it separately
    tasklistCommand = 'tasklist /FI "ImageName eq explorer.exe" /FI "Status eq Running" /FO LIST'
    tasklistProcess = subprocess.Popen(tasklistCommand, shell=True, stdout=subprocess.PIPE)
    line = tasklistProcess.stdout.readlines()[2]
    pidNum = int(line.decode().split()[-1])
    title = self.getAppTitle(pidNum)
    app = {
      'pid': pidNum,
      'title': title,
      'windows': [],
    }
    apps.insert(0, app)

    # Complement the apps dictionary with corresponding running windows
    win32gui.EnumWindows(self.winEnumHandler, None)
    for app in apps:
      for window in self.runningWindows:
        if window['parentPid'] == app['pid']:
          app['windows'].append(window)
    return apps

  # Switches to the window specified by the give n PID.
  def switchToWindow(self, pid):
    try:
      app = Application().connect(process=pid)
      app.top_window().set_focus()
    except:
      print(f'Switching to window with PID: {pid} failed.')

  # Shows the app switcher.
  def showAppSwitcher(self):
    self.prevWindowPid = self.getForegroundWindowPid()
    apps = self.getRunningAppsAndWindows()
    self.appsUi.updateList(apps)
    self.appsUi.show()
    # self.ui.Iconize(False)
    self.switchToWindow(self.appsWindowPid)
    self.appsUi.Raise()

  # Hides the app switcher and switches to the window which was previously in the foreground.
  def hideAppSwitcherAndShowPrevWindow(self):
    self.hideAppSwitcher()
    self.switchToWindow(self.prevWindowPid)

  # Hides the app switcher.
  def hideAppSwitcher(self):
    self.appsUi.hide()

  # Called when switched out of the apps window.
  def windowDeactivated(self):
    self.hideAppSwitcher()

  # Exits the program.
  def exitSwitcher(self):
    self.appsUi.cleanAndClose()
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
            # running showAppSwitcher() in a new thread fixes the issue of Win key not being released after calling showAppSwitcher()
            thread = Thread(target=self.showAppSwitcher)
            thread.start()
            # timer.start()
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
  switcher.setAppsAppsUI(mainFrame)
  switcher.getRunningAppsAndWindows()
  with keyboard.Listener(on_press=switcher.onKeyDown, on_release=switcher.onKeyUp) as listener:
    app.MainLoop()
    listener.join()
    del app

main()
