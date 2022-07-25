import subprocess
import sys
from threading import Thread
import win32api

import psutil
from pynput import keyboard
from pywinauto import Application
import wx

from util import Util
from config import Config
from gui import MainFrame

# Main application class.
class WinSwitcher:

  # Initializes the object.
  def __init__(self, config):
    self.config = config  
    self.pressedKeys = set()
    self.appsPid= Util.getActiveWindowPid()
    self.lastWindowPid = self.appsPid

      # Sets the UI object for this runner.
  def setAppsAppsUI(self, ui):
    self.appsUi = ui

  def switchToApp(self, pid):
    try:
      app = Application().connect(process=pid)
      app.top_window().set_focus()
    except:
      print(f'Switching to window with PID: {pid} failed.')

  def showAppSwitcher(self):
    self.lastWindowPid = Util.getActiveWindowPid()
    apps = self.getRunningApps()
    self.appsUi.updateList(apps)
    self.appsUi.show()
    # self.ui.Iconize(False)
    self.switchToApp(self.appsPid)
    self.appsUi.Raise()

  def hideAppSwitcherAndShowLastWindow(self):
    self.hideAppSwitcher()
    self.switchToApp(self.lastWindowPid)

  def hideAppSwitcher(self):
    print('Hiding')
    self.appsUi.hide()

  def windowDeactivated(self):
    self.hideAppSwitcher()


  def exitSwitcher(self):
    self.appsUi.cleanAndClose()
    sys.exit()

  def onKeyDown(self, key):
    self.pressedKeys.add(key)

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

  # Returns the name of the app specified by PID
  def getAppTitle(self, pid):
    process = psutil.Process(pid)
    path = process.exe()
    langs = win32api.GetFileVersionInfo(path, r'\VarFileInfo\Translation')
    key = r'StringFileInfo\%04x%04x\FileDescription' % (langs[0][0], langs[0][1])
    title = (win32api.GetFileVersionInfo(path, key))
    return title

  # Get the list of running apps names and their PIDs.
  def getRunningApps(self):
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
        if name in ['ApplicationFrameHost', 'SystemSettings', 'TextInputHost']:
          continue

        pidNum = int(pid)
        title = self.getAppTitle(pidNum)
        app = {'title': title, 'pid': pidNum}
        apps.append(app)
        print(f'{name} {pid} {title}')
      i = i + 1

    # File Explorer is not listed, so handle it separately
    tasklistCommand = 'tasklist /FI "ImageName eq explorer.exe" /FI "Status eq Running" /FO LIST'
    tasklistProcess = subprocess.Popen(tasklistCommand, shell=True, stdout=subprocess.PIPE)
    line = tasklistProcess.stdout.readlines()[2]
    pidNum = int(line.decode().split()[-1])
    title = self.getAppTitle(pidNum)
    app = {'title': title, 'pid': pidNum}
    apps.insert(0, app)

    return apps

# Main function.
def main():
  app = wx.App()
  config = Config()
  switcher = WinSwitcher(config)
  mainFrame = MainFrame(switcher, config, title=MainFrame.WINDOW_TITLE)
  switcher.setAppsAppsUI(mainFrame)
  switcher.getRunningApps()
  with keyboard.Listener(on_press=switcher.onKeyDown, on_release=switcher.onKeyUp) as listener:
    app.MainLoop()
    listener.join()
    del app

main()
