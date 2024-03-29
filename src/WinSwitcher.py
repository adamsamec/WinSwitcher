import accessible_output2.outputs.auto
import os
from pathlib import Path
import psutil
from pynput import keyboard
from pywinauto import Application, mouse
import rich
import subprocess
import sys
import time
import win32api
import win32con
import win32gui
import win32process
import wx

from config import Config
from gui import MainFrame
from lang import _
from util import MyKey

# Main application class.
class WinSwitcher:

    # Window process filenames which to exclude from the list
    EXCLUDED_WINDOW_FILENAMES = [
        "ApplicationFrameHost.exe",
        "SystemSettings.exe",
        "TextInputHost.exe",
        "HxOutlook.exe",
        "ShellExperienceHost.exe",
    ]

    # Replacements for app titles to make them shorter or more readable
    REPLACED_APP_TITLES = {
        "Windows Command Processor": _("Command Prompt"),
        "WindowsTerminal": _("Command Prompt"),
    }

    # Initializes the object.
    def __init__(self, config):
        self.config = config
        self.sr = accessible_output2.outputs.auto.Auto()
        self.pressedKeys = set()
        self.openWindows = []
        self.hwnd = self.getForegroundWindowHwnd()
        self.prevWindowHwnd = self.hwnd

    # Returns the hwnd of the window in the foreground.
    def getForegroundWindowHwnd(self):
        hwnd = win32gui.GetForegroundWindow()
        return hwnd

    # Returns the title of the app specified by the given process path.
    def getAppTitle(self, path):
        langs = win32api.GetFileVersionInfo(path, r"\VarFileInfo\Translation")
        key = r"StringFileInfo\%04x%04x\FileDescription" % (langs[0][0], langs[0][1])
        title = win32api.GetFileVersionInfo(path, key)

        # If the title is missing, use the filename without the .exe extension instead
        name = os.path.splitext(Path(path).name)[0]
        if not title:
            title = name

        # Some titles are not the same as in Taskbar, so replace at least those we know about
        if title in list(WinSwitcher.REPLACED_APP_TITLES.keys()):
            title = WinSwitcher.REPLACED_APP_TITLES[title]

        return title

    # Returns the path for the process specified by the given window hwnd.
    def getProcessPath(self, hwnd):
        threadId, processId = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(processId)
        path = process.exe()
        return path

    # Handler which is called for each open window and saves its information.
    def winEnumHandler(self, hwnd, ctx):
        # Do not include the switcher window in the list
        if hwnd == self.guiHwnd:
            return
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd)
        if not title:
            return
        path = self.getProcessPath(hwnd)
        filename = Path(path).name
        if filename in WinSwitcher.EXCLUDED_WINDOW_FILENAMES:
            return
        window = {
            "hwnd": hwnd,
            "path": path,
            "filename": filename,
            "title": title,
        }
        self.openWindows.append(window)

    # Updates the list of the currently open windows.
    def updateOpenWindows(self):
        self.openWindows = []
        win32gui.EnumWindows(self.winEnumHandler, None)

        # Remove the File Explorer desktop item
        window = self.openWindows[-1]
        if (window["filename"] == "explorer.exe") and (
            window["title"] == "Program Manager"
        ):
            del self.openWindows[-1]

    # Returns a list of running apps where each app consists of info about itss last window hwnd, process path and filename, app title and its open windows.
    def getRunningAppsAndWindows(self):
        self.updateOpenWindows()
        apps = []
        appIndexes = {}
        appIndex = 0

        for window in self.openWindows:
            appKey = window["path"]
            try:
                appIndexes[appKey]

                # We are on a window for which we've already created an ap, so add the window to that appp
                app = apps[appIndexes[appKey]]
                app["windows"].append(window)

            except KeyError:
                # We are on  a window for which we've not yet created an app, so create the app and save the index for that app
                lastWindowHwnd = window["hwnd"]
                path = window["path"]
                filename = Path(path).name

                # Rename the File Explorer app
                if filename == "explorer.exe":
                    title = _("File Explorer")
                else:
                    title = self.getAppTitle(path)
                app = {
                    "lastWindowHwnd": lastWindowHwnd,
                    "path": path,
                    "filename": filename,
                    "title": title,
                    "windows": [window],
                }
                apps.append(app)
                appIndexes[appKey] = appIndex
                appIndex += 1
        # rich.print(apps)
        return apps

    # Returns a list of open windows for the app with the given last window hwnd.
    def getAppWindows(self, lastWindowHwnd):
        self.updateOpenWindows()
        path = self.getProcessPath(lastWindowHwnd)
        windows = []
        for window in self.openWindows:
            if window["path"] == path:
                windows.append(window)
        return windows

    # Switches to WinSwitcher.
    def switchToSwitcher(self):
        # Mouse movement out of the screen bypasses the Windows system windows switching restriction
        mouse.move(coords=(-10000, 500))
        self.switchToWindow(self.hwnd)

    # Switches to the window specified by the given hwnd.
    def switchToWindow(self, hwnd):
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            win32gui.SetForegroundWindow(hwnd)
        except:
            print(f"Switching to window with handle: {hwnd} failed.")

    # Quits the app specified by the given last window hwnd.
    def quitApp(self, lastWindowHwnd):
        self.srOutput(_("Quitting the app"), True)
        threadId, processId = win32process.GetWindowThreadProcessId(lastWindowHwnd)
        process = psutil.Process(processId)
        filename= process.name()

        # In case of File Explorer, don't kill the explorer.exe process but rather close its windows one by one
        if filename == "explorer.exe":
            windows = self.getAppWindows(lastWindowHwnd)
            for window in windows:
                self.closeWindow(window["hwnd"], False)
            return

            # In case of other apps, kill the process softly
        app = Application().connect(process=processId)
        app.kill(True)

    # Closes the window specified by the given hwnd and returns if the closing was successfull.
    def closeWindow(self, hwnd, srOutput=True):
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        if srOutput:
            self.srOutput(_("Closing the window"), True)

        # Give some time for closing and then check if closing succeeded
        time.sleep(1)
        self.updateOpenWindows()
        for window in self.openWindows:
            if window["hwnd"] == hwnd:
                if srOutput:
                    self.srOutput(_("Closing failed"), True)
                return False
        return True

    # Shows the app switcher.
    def showSwitcher(self, type, args=None):
        foregroundWindowHwnd = self.getForegroundWindowHwnd()
        isStayingInSwitcher = foregroundWindowHwnd == self.guiHwnd
        if not isStayingInSwitcher:
            # Save the previous window hwnd if not switching from apps list to windows list or vice versa, that is, if not staying in WinSwitcher
            self.prevWindowHwnd = foregroundWindowHwnd

        if type == "apps":
            apps = self.getRunningAppsAndWindows()
            self.ui.updateListUsingApps(apps)
        elif type == "windows":
            hwnd = (
                foregroundWindowHwnd if not isStayingInSwitcher else self.prevWindowHwnd
            )
            windows = self.getAppWindows(hwnd)
            self.ui.updateListUsingForegroundAppWindows(windows)
        self.ui.show()
        if isStayingInSwitcher:
            return
        # self.ui.Iconize(False)
        self.switchToSwitcher()
        self.ui.Raise()

    # Hides the switcher and switches to the window which was previously in the foreground.
    def hideSwitcherAndShowPrevWindow(self):
        self.hideSwitcher()
        self.switchToWindow(self.prevWindowHwnd)

    # Hides the switcher.
    def hideSwitcher(self):
        self.ui.hide()

    # Called when switched out of the apps window.
    def windowDeactivated(self):
        self.hideSwitcher()

    # Cleans everything, including saving the settings to the config file, and exits the program.
    def exitSwitcher(self):
        self.srOutput(_("Exiting WinSwitcher"), True)
        self.config.saveToFile()
        self.ui.cleanAndClose()

        # Give some time to finish the speech before exiting
        time.sleep(3)
        sys.exit()

    # Called when key is pressed.
    def onKeyDown(self, key):
        key = MyKey(key)
        self.pressedKeys.add(key)

    # Called when key is released.
    def onKeyUp(self, key):
        key = MyKey(key)
        shortcuts = self.config.getShortcuts()
        for shortcut in shortcuts:
            for keys in shortcut["keys"]:
                if keys <= self.pressedKeys:
                    command = shortcut["command"]
                    if command == "showApps":
                        self.showSwitcher("apps")
                    elif command == "showWindows":
                        self.showSwitcher("windows")

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
        self.srOutput(_("WinSwitcher started"), True)
        with keyboard.Listener(
            on_press=self.onKeyDown, on_release=self.onKeyUp
        ) as self.listener:
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
