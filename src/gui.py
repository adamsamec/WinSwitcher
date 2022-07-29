import markdown2
import wx

from lang import _

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

    # Running apps or windows listbox
    runningListboxHbox = wx.BoxSizer(wx.HORIZONTAL)
    self.runningLabel = wx.StaticText(self.panel, -1, _('Running apps'))
    runningListboxHbox.Add(self.runningLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
    self.runningListbox = wx.ListBox(self.panel, size=(100, 0), choices = [], style = wx.LB_SINGLE)
    self.runningListbox.Bind(wx.EVT_CHAR_HOOK, self.onRunningListboxCharHook)
    runningListboxHbox.Add(self.runningListbox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    bottomButtonsHbox = wx.BoxSizer(wx.HORIZONTAL)

        # Help button
    self.helpButton = wx.Button(self.panel, label=_('Help'))
    self.helpButton.Bind(wx.EVT_BUTTON, self.onHelpButtonClick)
    bottomButtonsHbox.Add(self.helpButton, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    vbox.Add(runningListboxHbox)
    vbox.Add(bottomButtonsHbox)
    self.panel.SetSizer(vbox)

  # Shows the window.
  def show(self):
    self.Centre()
    self.Show()
    self.Fit()
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
    if not event.GetActive():
      self.switcher.windowDeactivated()
    event.Skip()

  # Handles  the key press events for the whole frame.
  def charHook(self, event):
    key = event.GetKeyCode()
    
    # Escape
    if key == wx.WXK_ESCAPE:
      self.switcher.hideSwitcherAndShowPrevWindow()
    else:
      event.Skip()
    
  # Handles  the key press events for the running apps and windows listbox.
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
      self.updateListUsingApps(self.runningApps)
    else:
      event.Skip()

  # Handles the help button click.
  def onHelpButtonClick(self, event):
    helpTitle = _('Help')
    helpDialog = HelpHTMLDialog(title=f'{helpTitle}{MainFrame.WINDOW_TITLE_SEPARATOR}{MainFrame.WINDOW_TITLE}', parent = self)

  # Update the running apps or windows listbox with the given running apps.
  def updateListUsingApps(self, apps):
    self.runningApps = apps
    self.runningListbox.Clear()
    for app in apps:
      self  .runningListbox.Append(app['title'])
    if self.showing == 'selectedAppWindows':
      self  .runningListbox.SetSelection(self.runningAppsSelection)
    else:
      self  .runningListbox.SetSelection(0)
    self.runningLabel.SetLabel(_('Running apps'))
    self.showing= 'runningApps'

  # Update the running apps or windows listbox with the given open windows.
  def updateListUsingWindows(self, windows):
    self.runningListbox.Clear()
    for window in windows:
      self  .runningListbox.Append(window['title'])
    self  .runningListbox.SetSelection(0)

  # Update the running apps or windows listbox with the open windows for the selected app.
  def updateListUsingSelectedAppWindows(self):
    self.runningAppsSelection = self.runningListbox.GetSelection()
    windows = self.runningApps[self.runningAppsSelection]['windows']
    self.updateListUsingWindows(windows)
    self.showing = 'selectedAppWindows'

  # Update the running apps or windows listbox with the given running windows for the app currently in the foreground.
  def updateListUsingForegroundAppWindows(self, windows):
    self.updateListUsingWindows(windows)
    self.foregroundAppWindows = windows
    self.runningLabel.SetLabel(_('Open windows'))
    self.showing = 'foregroundAppWindows'

  # Switch to the app currently selected in the apps listbox.
  def switchToSelectedApp(self):
    selection = self.runningListbox.GetSelection()
    app = self.runningApps[selection]
    self.switcher.switchToApp(app)

  # Switch to the selected app window currently selected in the running apps or windows listbox.
  def switchToSelectedAppSelectedWindow(self):
    selection= self.runningListbox.GetSelection()
    windows = self.runningApps[self.runningAppsSelection]['windows']
    hwnd = windows[selection]['hwnd']
    self.switcher.switchToWindow(hwnd)

  # Switch to the foreground app window currently selected in the running apps or windows listbox.
  def switchToForegroundAppSelectedWindow(self):
    selection= self.runningListbox.GetSelection()
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
    
  # Handles  the key press events for the whole dialog.
  def charHook(self, event):
    key = event.GetKeyCode()
    
    # Escape
    if key == wx.WXK_ESCAPE:
      self.close()
    else:
      event.Skip()
