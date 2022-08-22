import json
import os
from pynput.keyboard import Key, KeyCode

from util import MyKey

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
    {Key.cmd, Key.shift_l, MyKey(KeyCode(char='A'))},
    {Key.cmd, Key.shift_r, MyKey(KeyCode(char='A'))},
],
    'Ctrl+Shift+1': [
      {Key.ctrl_l, Key.shift_l, MyKey(KeyCode(vk=49))},
      {Key.ctrl_r, Key.shift_l, MyKey(KeyCode(vk=49))},
      {Key.ctrl_l, Key.shift_r, MyKey(KeyCode(vk=49))},
      {Key.ctrl_r, Key.shift_r, MyKey(KeyCode(vk=49))},
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
    {Key.cmd, Key.shift_l, MyKey(KeyCode(char='W'))},
    {Key.cmd, Key.shift_r, MyKey(KeyCode(char='W'))},
],
    'Ctrl+Shift+2': [
      {Key.ctrl_l, Key.shift_l, MyKey(KeyCode(vk=50))},
      {Key.ctrl_r, Key.shift_l, MyKey(KeyCode(vk=50))},
      {Key.ctrl_l, Key.shift_r, MyKey(KeyCode(vk=50))},
      {Key.ctrl_r, Key.shift_r, MyKey(KeyCode(vk=50))},
    ],
},
},
]

  # Initializes the object by loading the configuration from file. If a configuration value exists in the config file at the standard writable application data directory (AppData on Windows), and if the file doesn't have old structure, it is used, otherwise the default configuration value is loaded from the default config file.
  def __init__(self):
    # Load the default config file
    config = self.loadFile(Config.DEFAULT_CONFIG_PATH)
     
    if os.path.exists(Config.APPDATA_CONFIG_PATH):
 # The application data config file exists
      appDataConfig = self.loadFile(Config.APPDATA_CONFIG_PATH)
      if not self.needsConfigUpdate(appDataConfig, config):
        # The application data config file structure is not old, so override the loaded default configuration values by the configuration values found in this application data config file
        self.override('settings', appDataConfig, config)
    else:
      # The application data  config file does not exist, so check if switcher's directory exists in the standard writable application data directory and create it if not
      directory = os.path.dirname(Config.APPDATA_CONFIG_PATH)
      if not os.path.isdir(directory):
        os.makedirs(directory)
      
    # Save the determined configuration and version to this object sattributes
    self.settings = config['settings']
    self.version = config['version']

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

  # Finds out whether the given application data configuration is old and thus needs to be updated (be completely overriden) by the given default configuration. This is done by comparing the versions of the two configurations.
  def needsConfigUpdate(self, appDataConfig, defaultConfig):
    appDataVersion = [int(part) for part in appDataConfig['version'].split('.')]
    defaultVersion = [int(part) for part in defaultConfig['version'].split('.')]

    # Update is needed if the major or first minor versions are lower, that is, if only the second minor version is lower, it will not result in the need for update
    return (appDataVersion[0] < defaultVersion[0]) or (appDataVersion[1] < defaultVersion[1])
    
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
        'version': self.version,
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
