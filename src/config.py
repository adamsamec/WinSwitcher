from pynput.keyboard import Key

# Class for getting application configuration.
class Config:

  # Keyboard shortcuts definitions.
  SHORTCUTS = [
{
'keys': [
    {Key.cmd, Key.f12},
],
'command': 'showApps',
},
{
'keys': [
    {Key.cmd, Key.f4},
],
'command': 'exit',
},
]

  def getShortcuts(self):
    return self.SHORTCUTS
