using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Windows.Controls;

namespace WinSwitcher
{
    /// <summary>
    /// Application configuration
    /// </summary>
    public class Config
    {
        private const string _defaultFilename = "App.config.default.json";
        private const string _filename = "App.config.json";
        private string _folder = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "WinSwitcher");
        private string _path;
        private ConfigJson _config;

        public Settings Settings
        {
            get { return _config.settings; }
        }

        public void Load()
        {
            Directory.CreateDirectory(_folder);
            string defaultPath = Path.Combine(Directory.GetCurrentDirectory(), _defaultFilename);
            _path = Path.Combine(_folder, _filename);

            // Create the config if it not yet exists
            if (!File.Exists(_path))
            {
                File.Copy(defaultPath, _path);
            }

            // Try to load the config
            string configString = File.ReadAllText(_path, Encoding.UTF8);
            _config = JsonSerializer.Deserialize<ConfigJson>(configString);
            Settings settings = _config.settings;

            string defaultConfigString = File.ReadAllText(defaultPath, Encoding.UTF8);
            ConfigJson defaultConfig = JsonSerializer.Deserialize<ConfigJson>(defaultConfigString);
            Settings defaultSettings = defaultConfig.settings;

            // Set missing JSON properties to defaults
            Utils.SetYesOrNo(settings, defaultSettings, ["launchOnStartup", "filterByTyping"]);
            if (settings.enabledShortcuts == null)
            {
                settings.enabledShortcuts = defaultSettings.enabledShortcuts;
            }
            else
            {
                if (settings.enabledShortcuts.showApps == null)
                {
                    settings.enabledShortcuts.showApps = defaultSettings.enabledShortcuts.showApps;
                }
                if (settings.enabledShortcuts.showWindows == null)
                {
                    settings.enabledShortcuts.showWindows = defaultSettings.enabledShortcuts.showWindows;
                }
            }
            Utils.SetYesOrNo(settings.enabledShortcuts.showApps, defaultSettings.enabledShortcuts.showApps, ["Win_F12", "Win_Shift_A"]);
            Utils.SetYesOrNo(settings.enabledShortcuts.showWindows, defaultSettings.enabledShortcuts.showWindows, ["Win_F11", "Win_Shift_W"]);
            Save();
        }

        public void Save()
        {
            var options = new JsonSerializerOptions { WriteIndented = true };
            string configString = JsonSerializer.Serialize(_config, options);
            File.WriteAllText(_path, configString, Encoding.UTF8);
        }
    }
}

