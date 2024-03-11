using System;
using System.IO;
using System.Text;
using System.Text.Json;
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

        private ConfigJson _configJson;

        public Settings Settings {
            get { return _configJson.settings; }
        }

        public void Load()
        {
            // Create config if it not yet exists
            Directory.CreateDirectory(_folder);
            string defaultPath = Path.Combine(Directory.GetCurrentDirectory(), _defaultFilename);
            string path = Path.Combine(_folder, _filename);
            if (!File.Exists(path)) { 
            File.Copy(defaultPath, path);
            }

            // Load the config
            string defaultConfigString = File.ReadAllText(path, Encoding.UTF8);
            ConfigJson defaultConfig = JsonSerializer.Deserialize<ConfigJson>(defaultConfigString);


        }
    }
}

