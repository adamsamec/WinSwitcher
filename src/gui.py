import wx

from lang import _
import util

# Main frame class.
class MainFrame(wx.Frame):

    WINDOW_TITLE = "WinSwitcher"
    SETTINGS_DIALOG_TITLE = _("Settings for WinSwitcher")

    # Initializes the object by linking it with the given WinSwitcher and Config objects, binding the event handlers, and creating the GUI.
    def __init__(self, switcher, config, title, parent=None):
        style = (
            wx.DEFAULT_FRAME_STYLE
            & (~wx.CLOSE_BOX)
            & (~wx.MINIMIZE_BOX)
            & (~wx.MAXIMIZE_BOX)
        )
        super(MainFrame, self).__init__(
            parent, title=title, size=(1000, 600), style=style
        )
        self.switcher = switcher
        self.config = config
        self.settingsDialog = None
        self.openingSettings = False
        self.appsFilterText = ""
        self.selectionMapping = {}
        self.showing = None

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_ACTIVATE, self.onActivate)
        self.Bind(wx.EVT_CHAR_HOOK, self.charHook)

        self.addWidgets()

    # Adds all the initial widgets to this frame.
    def addWidgets(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Filter textbox
        filterHbox = wx.BoxSizer(wx.HORIZONTAL)
        filterLabel = wx.StaticText(self.panel, wx.ID_ANY, _("Filter"))
        filterHbox.Add(filterLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.filterTextbox = wx.TextCtrl(self.panel, size=(800, 0))
        self.filterTextbox.Bind(wx.EVT_CHAR_HOOK, self.onFilterTextboxCharHook)
        self.filterTextbox.Bind(wx.EVT_TEXT, self.onFilterTextboxChange)
        filterHbox.Add(self.filterTextbox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        # Running apps or windows listbox
        runningVbox = wx.BoxSizer(wx.VERTICAL)
        self.runningLabel = wx.StaticText(self.panel, wx.ID_ANY, _("Running apps"))
        runningVbox.Add(self.runningLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        self.runningListbox = wx.ListBox(
            self.panel, size=(1200, 500), choices=[], style=wx.LB_SINGLE
        )
        self.runningListbox.Bind(wx.EVT_CHAR_HOOK, self.onRunningListboxCharHook)
        self.runningListbox.Bind(wx.EVT_KEY_DOWN, self.onRunningListboxKeyDown)
        runningVbox.Add(self.runningListbox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

        # Bottom buttons
        bottomButtonsHbox = wx.BoxSizer(wx.HORIZONTAL)

        # Settings button
        self.settingsButton = wx.Button(self.panel, label=_("Settings"))
        self.settingsButton.Bind(wx.EVT_BUTTON, self.onSettingsButtonClick)
        bottomButtonsHbox.Add(
            self.settingsButton, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5
        )

        vbox.Add(bottomButtonsHbox)
        vbox.Add(filterHbox)
        vbox.Add(runningVbox)
        self.panel.SetSizer(vbox)

    # Shows the window.
    def show(self):
        self.Centre()
        self.Show()
        self.Fit()
        self.resetFilter()
        self.runningListbox.SetFocus()

    # Hides the window.
    def hide(self):
        self.Hide()
        self.showing = None

        # Cleans everything and destroys the window.

    def cleanAndClose(self):
        if self.settingsDialog:
            self.settingsDialog.close()
        wx.CallAfter(self.Destroy)

    # Handles  the window close event.
    def onClose(self, event):
        self.switcher.exitSwitcher()

    # Handles the window activate and deactivate events.
    def onActivate(self, event):
        if event.GetActive():
            self.runningListbox.SetFocus()
        else:
            if self.settingsDialog:
                self.settingsDialog.close()
            if not self.openingSettings:
                self.switcher.windowDeactivated()
        event.Skip()

    # Handles  the key press event for the whole frame.
    def charHook(self, event):
        key = event.GetKeyCode()
        modifiers = event.GetModifiers()
        onlyControlDown = modifiers == wx.MOD_CONTROL

        # Escape
        if key == wx.WXK_ESCAPE:
            self.switcher.hideSwitcherAndShowPrevWindow()

            # Control + F
        elif (key == ord("F")) and onlyControlDown:
            self.filterTextbox.SetFocus()

        else:
            event.Skip()

    # Handles  the key press event for the filter textbox.
    def onFilterTextboxCharHook(self, event):
        key = event.GetKeyCode()

        # Enter
        if key == wx.WXK_RETURN:
            self.runningListbox.SetFocus()

        else:
            event.Skip()

    # Handles  the text change event for the filter textbox.
    def onFilterTextboxChange(self, event):
        if self.showing:
            if False and self.showing == "selectedAppWindows":
                self.updateListUsingApps(resetFilter=False)
                # self.updateList("runningApps")
            else:
                self.updateList(self.showing)
            self.setDefaultSelection()
        event.Skip()

    # Handles  the key press event for the running apps and windows listbox.
    def onRunningListboxCharHook(self, event):
        key = event.GetKeyCode()

        # Enter
        if key == wx.WXK_RETURN:
            if self.showing == "runningApps":
                self.switchToSelectedApp()
            elif self.showing == "selectedAppWindows":
                self.switchToSelectedAppSelectedWindow()
            elif self.showing == "foregroundAppWindows":
                self.switchToForegroundAppSelectedWindow()

        # Right arrow
        if (key == wx.WXK_RIGHT) and (self.showing == "runningApps"):
            self.updateListUsingSelectedAppWindows()

        # Left arrow
        if (key == wx.WXK_LEFT) and (self.showing == "selectedAppWindows"):
            self.updateListUsingApps(resetFilter=False)

        else:
            event.Skip()

    # Handles  the key down event for the running apps and windows listbox.
    def onRunningListboxKeyDown(self, event):
        key = event.GetKeyCode()

        # Right or Left arrow
        if (key == wx.WXK_RIGHT) or (key == wx.WXK_LEFT):
            # Disable the navigation behavior  for the Right and Left arrow keys
            pass

        else:
            event.Skip()

    # Handles the settings button click.
    def onSettingsButtonClick(self, event):
        self.openingSettings = True
        self.settingsDialog = SettingsDialog(
            self.switcher,
            self.config,
            title=MainFrame.SETTINGS_DIALOG_TITLE,
            parent=self,
        )
        self.openingSettings = False

    # Clears the text of the filter textbox.
    def resetFilter(self):
        self.filterTextbox.SetValue("")

    # Sets the running apps and windows listbox selection to the default value, i.e., to the firs item in the listbox if not empty.
    def setDefaultSelection(
        self,
    ):
        if self.runningListbox.GetCount() >= 0:
            self.runningListbox.SetSelection(0)

    # Returns for the given list name the app or window selection index derived from the item currently selected in the running apps and windows listbox.
    def getMappedSelection(self, listName):
        selection = self.runningListbox.GetSelection()
        if selection < 0:
            return selection
        return self.selectionMapping[listName][selection]

    # Updates the running apps or windows listbox with the filter applied.
    def updateList(self, showing):
        filterText = self.filterTextbox.GetValue().strip()
        self.runningListbox.Clear()

        # If the filter text is empty, fil the listbox with all the items
        if len(filterText) == 0:
            if showing == "runningApps":
                for app in self.runningApps:
                    self.runningListbox.Append(app["titleAndCount"])
                length = len(self.runningApps)
                self.selectionMapping["appsAndForegroundAppWindows"] = range(length)
            elif showing == "selectedAppWindows":
                windows = self.runningApps[self.runningAppsMappedSelection]["windows"]
                for window in windows:
                    self.runningListbox.Append(window["title"])
                length = len(windows)
                self.selectionMapping["selectedAppWindows"] = range(length)
            elif showing == "foregroundAppWindows":
                for window in self.foregroundAppWindows:
                    self.runningListbox.Append(window["title"])
                length = len(self.foregroundAppWindows)
                self.selectionMapping["appsAndForegroundAppWindows"] = range(length)
            return

        # Filter text is not empty, so fill the listbox with filtred items
        if showing == "runningApps":
            self.selectionMapping["appsAndForegroundAppWindows"] = []
            for index, app in enumerate(self.runningApps):
                if util.isFoundNotSensitive(filterText, app["title"]):
                    self.runningListbox.Append(app["titleAndCount"])
                    self.selectionMapping["appsAndForegroundAppWindows"].append(index)
        elif showing == "selectedAppWindows":
            self.selectionMapping["selectedAppWindows"] = []
            windows = self.runningApps[self.runningAppsMappedSelection]["windows"]
            for index, window in enumerate(windows):
                if util.isFoundNotSensitive(filterText, window["title"]):
                    self.runningListbox.Append(window["title"])
                    self.selectionMapping["selectedAppWindows"].append(index)
        elif showing == "foregroundAppWindows":
            self.selectionMapping["appsAndForegroundAppWindows"] = []
            for index, window in enumerate(self.foregroundAppWindows):
                if util.isFoundNotSensitive(filterText, window["title"]):
                    self.runningListbox.Append(window["title"])
                    self.selectionMapping["appsAndForegroundAppWindows"].append(index)

    # Updates the running apps or windows listbox with the given running apps.
    def updateListUsingApps(self, apps=None, resetFilter=True):
        self.filterTextbox.SetValue(self.appsFilterText)
        if apps:
            self.runningApps = apps
        self.runningLabel.SetLabel(_("Running apps"))
        # if resetFilter:
        # self.resetFilter()
        self.updateList("runningApps")
        if self.showing == "selectedAppWindows":
            self.runningListbox.SetSelection(self.runningAppsSelection)
        else:
            self.setDefaultSelection()
        self.showing = "runningApps"

    # Updates the running apps or windows listbox with the open windows for the selected app.
    def updateListUsingSelectedAppWindows(self):
        self.runningAppsMappedSelection = self.getMappedSelection(
            "appsAndForegroundAppWindows"
        )
        self.runningAppsSelection = self.runningListbox.GetSelection()

        # Save the filter text and reset the filter
        self.appsFilterText = self.filterTextbox.GetValue()
        self.resetFilter()

        self.runningLabel.SetLabel(_("Open windows"))
        self.updateList("selectedAppWindows")
        self.setDefaultSelection()
        self.showing = "selectedAppWindows"

    # Updates the running apps or windows listbox with the given open windows for the app currently in the foreground.
    def updateListUsingForegroundAppWindows(self, windows):
        self.runningLabel.SetLabel(_("Open windows"))
        self.foregroundAppWindows = windows
        self.updateList("foregroundAppWindows")
        self.setDefaultSelection()
        self.showing = "foregroundAppWindows"

    # Switch to the app currently selected in the apps listbox.
    def switchToSelectedApp(self):
        selection = self.getMappedSelection("appsAndForegroundAppWindows")
        hwnd = self.runningApps[selection]["lastWindowHwnd"]
        self.switcher.switchToWindow(hwnd)

    # Switch to the selected app window currently selected in the running apps or windows listbox.
    def switchToSelectedAppSelectedWindow(self):
        selection = self.getMappedSelection("selectedAppWindows")
        windows = self.runningApps[self.runningAppsMappedSelection]["windows"]
        hwnd = windows[selection]["hwnd"]
        self.switcher.switchToWindow(hwnd)

    # Switch to the foreground app window currently selected in the running apps or windows listbox.
    def switchToForegroundAppSelectedWindow(self):
        selection = self.getMappedSelection("appsAndForegroundAppWindows")
        hwnd = self.foregroundAppWindows[selection]["hwnd"]
        self.switcher.switchToWindow(hwnd)


# Settings dialog class.
class SettingsDialog(wx.Dialog):

    # Initializes the object by linking it with the given switcher and Config objects, binding the event handlers, and creating the GUI.
    def __init__(self, switcher, config, title, parent=None):
        super(SettingsDialog, self).__init__(parent=parent, title=title)
        self.switcher = switcher
        self.config = config

        self.Bind(wx.EVT_ACTIVATE, self.onActivate)
        self.Bind(wx.EVT_CHAR_HOOK, self.charHook)

        self.addWidgets()
        self.Centre()
        self.ShowModal()
        self.Fit()

    # Adds all the initial widgets to this dialog.
    def addWidgets(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        settings = self.config.settings

        # Enabled show apps shortcuts check list
        showAppsSbox = wx.StaticBoxSizer(
            wx.VERTICAL, self.panel, _("Enabled keyboard shortcuts for list of apps")
        )
        showAppsChoices = ["Windows + F12", "Windows + Shift + A", "Ctrl+Shift+1"]
        self.showAppsCheckList = wx.ListCtrl(showAppsSbox.GetStaticBox(), wx.ID_ANY, size=(400, 120), style=wx.LC_LIST)
        self.initShortcutsCheckList(self.showAppsCheckList, showAppsChoices, "showApps")
        self.showAppsCheckList.Bind(wx.EVT_LIST_ITEM_CHECKED, self.onShowAppsItemCheck)
        self.showAppsCheckList.Bind(
            wx.EVT_LIST_ITEM_UNCHECKED, self.onShowAppsItemUncheck
        )
        showAppsSbox.Add(
            self.showAppsCheckList, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5
        )

        # Enabled show windows shortcuts check list
        showWindowsSbox = wx.StaticBoxSizer(
            wx.VERTICAL, self.panel, _("Enabled keyboard shortcuts for list of windows")
        )
        showWindowsChoices = ["Windows + F11", "Windows + Shift + W", "Ctrl+Shift+2"]
        self.showWindowsCheckList = wx.ListCtrl(
            showWindowsSbox.GetStaticBox(), wx.ID_ANY, size=(400, 120), style=wx.LC_LIST
        )
        self.initShortcutsCheckList(
            self.showWindowsCheckList, showWindowsChoices, "showWindows"
        )
        self.showWindowsCheckList.Bind(
            wx.EVT_LIST_ITEM_CHECKED, self.onShowWindowsItemCheck
        )
        self.showWindowsCheckList.Bind(
            wx.EVT_LIST_ITEM_UNCHECKED, self.onShowWindowsItemUncheck
        )
        showWindowsSbox.Add(
            self.showWindowsCheckList, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5
        )

        # Bottom buttons
        bottomButtonsHbox = wx.BoxSizer(wx.HORIZONTAL)

        # Close button
        self.closeButton = wx.Button(self.panel, label=_("Close"))
        self.closeButton.SetDefault()
        self.closeButton.Bind(wx.EVT_BUTTON, self.onCloseButtonClick)

        bottomButtonsHbox.Add(
            self.closeButton, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5
        )

        vbox.Add(showAppsSbox)
        vbox.Add(showWindowsSbox)
        vbox.Add(bottomButtonsHbox)
        self.panel.SetSizer(vbox)

    # Closes the dialog.
    def close(self):
        self.Parent.settingsDialog = None
        self.Hide()
        self.Parent.show()
        # self.Destroy()

    # Handles the dialog activate and deactivate events.
    def onActivate(self, event):
        if event.GetActive():
            self.Parent.Hide()
        else:
            self.Hide()

    # Handles  the key press events for the whole dialog.
    def charHook(self, event):
        key = event.GetKeyCode()

        # Escape
        if key == wx.WXK_ESCAPE:
            self.close()
        else:
            event.Skip()

    # Handles the Close button click.
    def onCloseButtonClick(self, event):
        self.close()

    # Handles the show apps check list item check.
    def onShowAppsItemCheck(self, event):
        self.onShortcutsCheckListCheckChange(event.Index, True, "showApps")

    # Handles the show apps check list item uncheck.
    def onShowAppsItemUncheck(self, event):
        self.onShortcutsCheckListCheckChange(event.Index, False, "showApps")

    # Handles the show windows check list item check.
    def onShowWindowsItemCheck(self, event):
        self.onShortcutsCheckListCheckChange(event.Index, True, "showWindows")

    # Handles the show windows check list item uncheck.
    def onShowWindowsItemUncheck(self, event):
        self.onShortcutsCheckListCheckChange(event.Index, False, "showWindows")

    # Handles the shortcuts check list item at the given index checked state change for the given command.
    def onShortcutsCheckListCheckChange(self, index, doCheck, command):
        self.tryChangeShortcutCheckState(
            self.showAppsCheckList, index, doCheck, command
        )

    # Appends the given choices to the given check list and checks the enabled shortcuts for the given command by retrieving them from the settings.
    def initShortcutsCheckList(self, checkList, choices, command):
        for choice in choices:
            checkList.Append([choice])
        checkList.EnableCheckBoxes()
        checkList.Select(0)
        checkList.SetColumnWidth(0, 300)

        # Determine the enabled shortcuts from the settings and check the corresponding check list items
        for index, shortcut in enumerate(
            self.config.settings["enabledShortcuts"][command]
        ):
            if self.config.settings["enabledShortcuts"][command][shortcut]:
                checkList.CheckItem(index)

    # Sets the shortcut at the given index in the settings to the given checked state for the given command.
    def changeShortcutCheckState(self, index, doCheck, command):
        for settingsIndex, shortcut in enumerate(
            self.config.settings["enabledShortcuts"][command]
        ):
            if settingsIndex == index:
                self.config.settings["enabledShortcuts"][command][shortcut] = doCheck

    # Determines if the checked state of the item at the given index of the given shortcuts check list results in no shortcut being checked for the given command, and if so, reverts the shortcut to the checked state, otherwise updates the settings using the given checked state for the given shortcut.
    def tryChangeShortcutCheckState(self, checkList, index, doCheck, command):
        isAnyChecked = False
        for listIndex in range(checkList.GetItemCount()):
            if checkList.IsItemChecked(listIndex):
                isAnyChecked = True
                break
        if command == "showApps":
            if not isAnyChecked:
                # If no shortcut is selected for this command, revert the item determined by the given index to the checked state, and don't update the settings
                checkList.CheckItem(index)
                return

        self.changeShortcutCheckState(index, doCheck, command)
