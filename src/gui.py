import markdown2
import wx

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
    
    self.Bind(wx.EVT_CLOSE, self.onClose)
    self.Bind(wx.EVT_ACTIVATE, self.onActivate)
    self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
    
    self.addWidgets()
    
  # Adds all the initial widgets to this frame.
  def addWidgets(self):
    self.panel = wx.Panel(self)    
    vbox = wx.BoxSizer(wx.VERTICAL)

    # Running apps listbox
    listboxHbox = wx.BoxSizer(wx.HORIZONTAL)
    appsLabel = wx.StaticText(self.panel, -1, 'Running apps')
    listboxHbox.Add(appsLabel, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
    self.appsListbox = wx.ListBox(self.panel, size=(100, 0), choices = [], style = wx.LB_SINGLE)
    self.appsListbox.Bind(wx.EVT_KEY_UP, self.onAppsListboxKeyUp)
    listboxHbox.Add(self.appsListbox, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    bottomButtonsHbox = wx.BoxSizer(wx.HORIZONTAL)

        # Help button
    self.helpButton = wx.Button(self.panel, label='Help')
    self.helpButton.Bind(wx.EVT_BUTTON, self.onHelpButtonClick)
    bottomButtonsHbox.Add(self.helpButton, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)

    vbox.Add(listboxHbox)
    vbox.Add(bottomButtonsHbox)
    self.panel.SetSizer(vbox)

  # Shows the window.
  def show(self):
    self.Centre()
    self.Show()
    self.Fit()
    self.appsListbox.SetFocus()

  # Hides the window.
  def hide(self):
    self.Hide()
    
      # Cleans everything and closes the window.
  def cleanAndClose(self):
    try:
      self.Destroy()
    except:
      pass
  
  # Handles  the window close event.
  def onClose(self, event):
    self.switcher.hideAppSwitcherAndShowPrevWindow()

  # Handles the window activate or deactivate event.
  def onActivate(self, event):
    if not event.GetActive():
      self.switcher.windowDeactivated()
    event.Skip()

  # Handles  the key press events for the whole frame.
  def onKeyUp(self, event):
    key = event.GetKeyCode()
    
    # Escape
    if key == wx.WXK_ESCAPE:
      self.switcher.hideAppSwitcherAndShowLastWindow()
    else:
      event.Skip()
    
  def onAppsListboxKeyUp(self, event):
    key = event.GetKeyCode()
    
    # Enter
    if key == wx.WXK_RETURN:
      self.switchToSelectedApp()
    else:
      event.Skip()

  # Handles the help button click.
  def onHelpButtonClick(self, event):
    helpDialog = HelpHTMLDialog(title=f'Help{MainFrame.WINDOW_TITLE_SEPARATOR}{MainFrame.WINDOW_TITLE}', parent = self)

  # Update the running apps listbox
  def updateList(self, apps):
    self.apps = apps
    self.appsListbox.Clear()
    for app in apps:
      self  .appsListbox.Append(app['title'])

  # Switch to the app currently selected in the apps listbox.
  def switchToSelectedApp(self):
    pos = self.appsListbox.GetSelection()
    pid = self.apps[pos]['pid']
    self.switcher.switchToWindow(pid)

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
