import markdown2
import wx

from lang import _
import util
# Main frame class.
class MainFrame(wx.Frame):

  WINDOW_TITLE_SEPARATOR = ' | '
  WINDOW_TITLE = 'WinSwitcher'

  # Initializes the object by linking it with the given WinSwitcher and Config objects, binding the event handlers, and creating the GUI.
  def __init__(self, switcher, config, title, parent = None):
    style = wx.DEFAULT_FRAME_STYLE & (~wx.CLOSE_BOX) & (~wx.MINIMIZE_BOX) & (~wx.MAXIMIZE_BOX)
    super(MainFrame, self).__init__(parent, title=title, style=style)
    self.switcher = switcher
    self.config = config
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
    filterLabel = wx.StaticText(self.panel, -1, _('Filter'))
    filterHbox.Add(filterLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
    self.filterTextbox= wx.TextCtrl(self.panel)
    self.filterTextbox.Bind(wx.EVT_CHAR_HOOK, self.onFilterTextboxCharHook)
    self.filterTextbox.Bind(wx.EVT_TEXT, self.onFilterTextboxChange)
    filterHbox.Add(self.filterTextbox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    # Running apps or windows listbox
    runningHbox = wx.BoxSizer(wx.HORIZONTAL)
    self.runningLabel = wx.StaticText(self.panel, -1, _('Running apps'))
    runningHbox.Add(self.runningLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
    self.runningListbox = wx.ListBox(self.panel, size=(100, 0), choices = [], style = wx.LB_SINGLE)
    self.runningListbox.Bind(wx.EVT_CHAR_HOOK, self.onRunningListboxCharHook)
    self.runningListbox.Bind(wx.EVT_KEY_DOWN, self.onRunningListboxKeyDown)
    runningHbox.Add(self.runningListbox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    bottomButtonsHbox = wx.BoxSizer(wx.HORIZONTAL)

        # Help button
    self.helpButton = wx.Button(self.panel, label=_('Help'))
    self.helpButton.Bind(wx.EVT_BUTTON, self.onHelpButtonClick)
    bottomButtonsHbox.Add(self.helpButton, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    vbox.Add(filterHbox)
    vbox.Add(runningHbox)
    vbox.Add(bottomButtonsHbox)
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
    
      # Cleans everything and closes the window.
  def cleanAndClose(self):
    try:
      self.Destroy()
    except:
      pass
  
  # Handles  the window close event.
  def onClose(self, event):
    self.switcher.hideSwitcherAndShowPrevWindow()

  # Handles the window activate and deactivate events.
  def onActivate(self, event):
    if event.GetActive():
      self.runningListbox.SetFocus()
    else:
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
    elif (key == ord('F')) and onlyControlDown:
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
      if self.showing == 'selectedAppWindows':
        self.updateListUsingApps(resetFilter=False)
        self.updateList('runningApps')
      else:
        self.updateList(self.showing)
      self.setDefaultSelection()
    event.Skip()

  # Handles  the key press event for the running apps and windows listbox.
  def onRunningListboxCharHook(self, event):
    key = event.GetKeyCode()
    
    # Enter
    if key == wx.WXK_RETURN:
      if self.showing == 'runningApps':
        self.switchToSelectedApp()
      elif self.showing == 'selectedAppWindows':
        self.switchToSelectedAppSelectedWindow()
      elif self.showing == 'foregroundAppWindows':
        self.switchToForegroundAppSelectedWindow()

    # Right arrow
    if (key == wx.WXK_RIGHT) and (self.showing == 'runningApps'):
      self.updateListUsingSelectedAppWindows()

    # Left arrow
    if (key == wx.WXK_LEFT) and (self.showing == 'selectedAppWindows'):
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

  # Handles the help button click.
  def onHelpButtonClick(self, event):
    helpTitle = _('Help')
    helpDialog = HelpHTMLDialog(title=f'{helpTitle}{MainFrame.WINDOW_TITLE_SEPARATOR}{MainFrame.WINDOW_TITLE}', parent = self)

  # Resets the text of the filter textbox and the listbox selection mappings.
  def resetFilter(self):
    self.filterTextbox.SetValue('')

  # Sets the running apps and windows listbox selection to the default value, i.e., to the firs item in the listbox if not empty.
  def setDefaultSelection(self):
    if len(self.selectionMapping) > 0:
      self.runningListbox.SetSelection(0)

  # Returns the app or window selection index derived from the item currently selected in the running apps and windows listbox.
  def getMappedSelection(self):
    selection = self.runningListbox.GetSelection()
    return self.selectionMapping[selection] if selection >= 0 else selection

  # Updates the running apps or windows listbox with the filter applied.
  def updateList(self, showing):
    filterText = self.filterTextbox.GetValue().strip()
    mappedSelection = self.getMappedSelection()
    self.runningListbox.Clear()

    # If showing windows for the selected app, filter is ignored
    if showing == 'selectedAppWindows':
      windows = self.runningApps[mappedSelection]['windows']
      length = len(windows)
      self.selectionMapping= range(length)
      for window in windows:
        self  .runningListbox.Append(window['title'])
      return

    # If the filter text is empty, fil the listbox with all the items
    if len(filterText) == 0:
      if showing == 'runningApps':
        for app in self.runningApps:
          self  .runningListbox.Append(app['titleAndCount'])
        length = len(self.runningApps)
        self.selectionMapping= range(length)
      elif showing == 'foregroundAppWindows':
        for window in self.foregroundAppWindows:
          self  .runningListbox.Append(window['title'])
        length = len(self.foregroundAppWindows)
        self.selectionMapping= range(length)
      return

    # Filter text is not empty, so fill the listbox with filtred items
    self.selectionMapping = []
    if showing == 'runningApps':
      for index, app in enumerate(self.runningApps):
        if util.isFoundNotSensitive(filterText, app['title']):
          self.runningListbox.Append(app['titleAndCount'])
          self.selectionMapping.append(index)
    elif showing == 'foregroundAppWindows':
      for index, window in enumerate(self.foregroundAppWindows):
        if util.isFoundNotSensitive(filterText, window['title']):
          self.runningListbox.Append(window['title'])
          self.selectionMapping.append(index)

  # Updates the running apps or windows listbox with the given running apps.
  def updateListUsingApps(self, apps=None, resetFilter=True):
    if apps:
      self.runningApps = apps
    self.runningLabel.SetLabel(_('Running apps'))
    if resetFilter:
      self.resetFilter()
    self.updateList('runningApps')
    if self.showing == 'selectedAppWindows':
      self  .runningListbox.SetSelection(self.runningAppsSelection)
    else:
      self.setDefaultSelection()
    self.showing= 'runningApps'

  # Updates the running apps or windows listbox with the running windows for the selected app.
  def updateListUsingSelectedAppWindows(self):
    self.runningAppsMappedSelection = self.getMappedSelection()
    self.runningAppsSelection = self.runningListbox.GetSelection()
    self.updateList('selectedAppWindows')
    self.setDefaultSelection()
    self.showing = 'selectedAppWindows'

  # Updates the running apps or windows listbox with the given running windows for the app currently in the foreground.
  def updateListUsingForegroundAppWindows(self, windows):
    self.runningLabel.SetLabel(_('Running windows'))
    self.foregroundAppWindows = windows
    self.updateList('foregroundAppWindows')
    self.setDefaultSelection()
    self.showing = 'foregroundAppWindows'

  # Switch to the app currently selected in the apps listbox.
  def switchToSelectedApp(self):
    selection = self.getMappedSelection()
    app = self.runningApps[selection]
    self.switcher.switchToApp(app)

  # Switch to the selected app window currently selected in the running apps or windows listbox.
  def switchToSelectedAppSelectedWindow(self):
    selection= self.getMappedSelection()
    windows = self.runningApps[self.runningAppsMappedSelection]['windows']
    hwnd = windows[selection]['hwnd']
    self.switcher.switchToWindow(hwnd)

  # Switch to the foreground app window currently selected in the running apps or windows listbox.
  def switchToForegroundAppSelectedWindow(self):
    selection= self.getMappedSelection()
    hwnd = self.foregroundAppWindows[selection]['hwnd']
    self.switcher.switchToWindow(hwnd)

# Help HTML dialog class.
class HelpHTMLDialog(wx.Dialog):

  # Paths to Markdown pages directory and files
  MARKDOWN_PATH = 'md/'
  HELP_PAGE_PATH = MARKDOWN_PATH + 'help.md'

  # Initializes the object by creating the CEF  web browser and binding the event handlers.
  def __init__(self, title, parent = None):
    super(HelpHTMLDialog, self).__init__(parent = parent, title = title)
    
    self.SetSize((1000, 800))
    self.Bind(wx.EVT_CHAR_HOOK, self.charHook)
    self.addBrowser()
    
    self.Centre()
    self.ShowModal()
    
  # Adds the web browser to this dialog and binds the dialog close event.
  def addBrowser(self):
    self.panel = wx.Panel(self)
    self.Bind(wx.EVT_CLOSE, self.onClose)
    
    html = self.loadHTML()
    
  # Closes all CEF processes on dialog close.
  def onClose(self, event):
    event.Skip()
    
  # Loads the page in Markdown, converts it into HTML and returns it.
  def loadHTML(self):
    path = HelpHTMLDialog.HELP_PAGE_PATH
    content = ''
    with open(path, encoding='utf-8') as file:
      # Load file line by line
      while True:
        line = file.readline()
        content += line
        if not line:
          break
    
    # Convert the page from Markkdown to HTML
    md = markdown2.Markdown()
    html = md.convert(content)
    
    # Wrap the page content with the basic HTML structure.
    html = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
</head>
<body>
''' + html + '''
</body>
</html>
'''
    return html
    
  # Closes the dialog without any changes.
  def close(self):
    self.Destroy()
    
  # Handles  the key press event for the whole dialog.
  def charHook(self, event):
    key = event.GetKeyCode()
    
    # Escape
    if key == wx.WXK_ESCAPE:
      self.close()
    else:
      event.Skip()
