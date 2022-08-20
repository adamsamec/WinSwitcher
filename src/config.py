import json
import os
from pynput.keyboard import Key, KeyCode

# Class for loading and saving application configuration.
class Config:

  # Path to the config file with the default configuration values.
  DEFAULT_CONFIG_PATH = 'config.default.json'
  
  # Path to the config file in the standard writable application data directory (AppData on Windows with the actually used configuration values.
  APPDATA_CONFIG_PATH = os.environ['APPDATA'] + '\\WinSwitcher\\config.json'

  # Keyboard shortcuts definitions.
  SHORTCUTS = [
{
'command': 'showApps',
'keys': {
    'Win+F12': [
      {Key.cmd, Key.f12},
    ],
    'Win+Shift+A': [
    {Key.cmd, Key.shift_l, KeyCode(char='A')},
    {Key.cmd, Key.shift_r, KeyCode(char='A')},
],
},
},
{
'command': 'showWindows',
'keys': {
    'Win+F11': [
      {Key.cmd, Key.f11},
    ],
    'Win+Shift+W': [
    {Key.cmd, Key.shift_l, KeyCode(char='W')},
    {Key.cmd, Key.shift_r, KeyCode(char='W')},
],
},
},
]

  # Initializes the object by loading the configuration from file. If a configuration value exists in the config file at the standard writable application data directory (AppData on Windows), it is used, otherwise the default configuration value is loaded from the default config file.
  def __init__(self):
    # Load the default config file
    config = self.loadFile(Config.DEFAULT_CONFIG_PATH)
     
    if os.path.exists(Config.APPDATA_CONFIG_PATH):
 # The application data config file exists, override the loaded default configuration values by the configuration values found in this application data config file
      appDataConfig = self.loadFile(Config.APPDATA_CONFIG_PATH)
      self.override('settings', appDataConfig, config)
    else:
      # The application data  config file does not exist, so check if switcher's directory exists in the standard writable application data directory and create it if not
      directory = os.path.dirname(Config.APPDATA_CONFIG_PATH)
      if not os.path.isdir(directory):
        os.makedirs(directory)
      
    # Save the determined configuration to this object properties
    self.settings = config['settings']

  # Loads and parses the JSON file at the given path and returns the loaded dictionary.
  def loadFile(self, path):
    content = ''
    with open(path, encoding='utf-8') as file:
      # Load file line by line
      while True:
        line = file.readline()
        content += line
        if not line:
          break

    # Parse the file content as JSON
    config = json.loads(content)
    return config

  # Overrides the target's dictionary values under the given category key with the values from the source dictionary.
  def override(self, category, source, target):
    if category in source:
      for key in target[category]:
        # Check if the target key exists in the source and its value has the same type
        if (key in source[category]) and (type(source[category][key]) == type(target[category][key])):
          # Override the target's value with the source's one
          target[category][key] = source[category][key]

  # Saves the current internally stored configuration to the application data config file.
  def saveToFile(self):
    with open(Config.APPDATA_CONFIG_PATH, 'w', encoding='utf-8') as file:
      config = {
        'settings': self.settings,
      }
      json.dump(config, file, indent = 2)

  # Returns a shortcuts dictionary based on currently enabled shortcuts.
  def getShortcuts(self):
    shortcuts = []
    for definition in Config.SHORTCUTS:
      shortcut = {
        'command': definition['command'],
        'keys': [],
      }
      for name in definition['keys']:
        if self.settings['enabledShortcuts'][definition['command']][name]:
          shortcut['keys'] += definition['keys'][name]
      shortcuts.append(shortcut)
    return shortcuts
