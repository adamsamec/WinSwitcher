import accessible_output2.outputs.auto
from pathlib import Path
import rich
import subprocess
import sys
from threading import Thread
import time
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
    self.sr = accessible_output2.outputs.auto.Auto()
    self.pressedKeys = set()
    self.runningWindows = []

    hwnd = self.getForegroundWindowHwnd()
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    self.app = Application().connect(process=pid)
    self.prevWindowHwnd = hwnd

  # Returns the hwnd of the window in the foreground.
  def getForegroundWindowHwnd(self):
    hwnd = win32gui.GetForegroundWindow()
    return hwnd

  # Returns the title of the app specified by the given process path.
  def getAppTitle(self, path):
    langs = win32api.GetFileVersionInfo(path, r'\VarFileInfo\Translation')
    key = r'StringFileInfo\%04x%04x\FileDescription' % (langs[0][0], langs[0][1])
    title = (win32api.GetFileVersionInfo(path, key))
    return title
    
  # Returns the info about the app specified by the given last window hwnd.
  def getAppInfo(self, lastWindowHwnd):
    threadId, processId = win32process.GetWindowThreadProcessId(lastWindowHwnd)
    process = psutil.Process(processId)
    filename = process.name()
    path = process.exe()
    title = self.getAppTitle(path)
    if title in list(WinSwitcher.REPLACED_APP_TITLES.keys()):
      title = WinSwitcher.REPLACED_APP_TITLES[title]
    info= {
      'lastWindowHwnd': lastWindowHwnd,
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
      process = psutil.Process(processId)
      filename = process.name()
      if filename in WinSwitcher.EXCLUDED_WINDOW_FILENAMES:
        return
      path = process.exe()
      window = {
        'threadId': threadId,
        'processId': processId,
        'hwnd': hwnd,
        'filename': filename,
        'path': path,
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

  # Returns a list of running apps where each app consists of info about itss last window hwnd, process path and filename, app title and its running windows.
  def getRunningAppsAndWindows(self):
    self.updateRunningWindows()
    apps = []
    appIndexes = {}
    appIndex = 0

    for window in self.runningWindows:
      appKey = window['path']
      try:
        appIndexes[appKey]

        # We are on a window for which we've already created an ap, so add the window to that appp
        app = apps[appIndexes[appKey]]
        app['windows'].append(window)

      except KeyError:
        # We are on  a window for which we've not yet created an app, so create the app and save the index for that app
        lastWindowHwnd = window['hwnd']
        path = window['path']
        filename = Path(path).name
        title = self.getAppTitle(path)
        app = {
'lastWindowHwnd': lastWindowHwnd,
'path': path,
'filename': filename,
'title': title,
'windows': [window],
        }
        apps.append(app)
        appIndexes[appKey] = appIndex
        appIndex += 1

    # Add window count to the app title
    for app in apps:
      count = len(app['windows'])
      if app['filename'] == 'explorer.exe':
        # Do not count Desktop as a window of File Explorer
        count -= 1
      countText = _('{} windows').format(count)
      app['titleAndCount'] = f'{app["title"]} ({countText})'
    rich.print(apps)
    return apps

  # Returns a list of running windows for the app with the given last window hwnd.
  def getAppWindows(self, lastWindowHwnd):
    self.updateRunningWindows()
    app = self.getAppInfo(lastWindowHwnd)
    windows = []
    for window in self.runningWindows:
      if window['path'] == app['path']:
        windows.append(window)
    return windows

  # Switches to WinSwitcher.
  def switchToSwitcher(self):
    # self.app.top_window().set_focus()
    # return
    try:
      self.app.top_window().set_focus()
    except:
      print('Switching to WinSwitcher failed.')

  # Switches to the window specified by the given hwnd.
  def switchToWindow(self, hwnd):
    try:
      win32gui.SetForegroundWindow(hwnd)
    except:
        print(f'Switching to window with handle: {hwnd} failed.')

  # Shows the app switcher.
  def showSwitcher(self, type, args):
    foregroundWindowHwnd = self.getForegroundWindowHwnd()
    isStayingInSwitcher = foregroundWindowHwnd == self.guiHwnd
    if not isStayingInSwitcher:
      # Save the previous window hwnd if not switching from apps list to windows list or vice versa, that is, if not staying in WinSwitcher
      self.prevWindowHwnd = foregroundWindowHwnd

    if type == 'apps':
      apps = self.getRunningAppsAndWindows()
      self.ui.updateListUsingApps(apps)
    elif type == 'windows':
      hwnd = foregroundWindowHwnd if not isStayingInSwitcher else self.prevWindowHwnd
      windows = self.getAppWindows(hwnd)
      self.ui.updateListUsingForegroundAppWindows(windows)
    self.ui.show()
    if isStayingInSwitcher:
      return
    # self.ui.Iconize(False)
    self.switchToSwitcher()
    self.ui.Raise()

  # Hides the app switcher and switches to the window which was previously in the foreground.
  def hideSwitcherAndShowPrevWindow(self):
    self.hideSwitcher()
    self.switchToWindow(self.prevWindowHwnd)

  # Hides the app switcher.
  def hideSwitcher(self):
    self.ui.hide()

  # Called when switched out of the apps window.
  def windowDeactivated(self):
    self.hideSwitcher()

  # Cleans everything and exits the program.
  def exitSwitcher(self):
    self.ui.cleanAndClose()
    self.srOutput(_('Exitting WinSwitcher'), True)

    # Give some time to finish the speech before exitting
    time.sleep(3)
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

      # Sets the apps UI object for the switcher and saves its hwnd.
  def setUI(self, ui):
    self.ui = ui
    self.guiHwnd = ui.GetHandle()

  # Outputs the given text via screen reader, optionally interrupting the current output.
  def srOutput(self, text, interrupt=False):
    self.sr.output(text, interrupt=interrupt)

  # Starts the program by setting up global keyboard listener and initiating the main GUI loop.
  def start(self, app, ui):
    self.setUI(ui)
    self.srOutput(_('WinSwitcher started'), True)
    with keyboard.Listener(on_press=self.onKeyDown, on_release=self.onKeyUp) as listener:
      app.MainLoop()
      listener.join()

# Main function.
def main():
  app = wx.App()
  config = Config()
  switcher = WinSwitcher(config)
  mainFrame = MainFrame(switcher, config, title=MainFrame.WINDOW_TITLE)
  switcher.start(app, mainFrame)

main()
