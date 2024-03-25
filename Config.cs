using System.IO;
using System.Text;
using System.Text.Json;

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

        public const string TRUE = "yes";
        public const string FALSE = "no";

        public Settings Settings
        {
            get { return _config.settings; }
        }

        public Config()
        {
            Directory.CreateDirectory(_folder);
            var assemblyPath = System.Reflection.Assembly.GetExecutingAssembly().Location;
            var installFolder = System.IO.Path.GetDirectoryName(assemblyPath);
            var defaultPath = Path.Combine(installFolder, _defaultFilename);
            _path = Path.Combine(_folder, _filename);

            // Create the config if it not yet exists
            if (!File.Exists(_path))
            {
                File.Copy(defaultPath, _path);
            }

            // Load the config
            var configString = File.ReadAllText(_path, Encoding.UTF8);
            _config = JsonSerializer.Deserialize<ConfigJson>(configString);
            var settings = _config.settings;

            var defaultConfigString = File.ReadAllText(defaultPath, Encoding.UTF8);
            var defaultConfig = JsonSerializer.Deserialize<ConfigJson>(defaultConfigString);
            var defaultSettings = defaultConfig.settings;

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
            var configString = JsonSerializer.Serialize(_config, options);
            File.WriteAllText(_path, configString, Encoding.UTF8);
        }
    }
}

