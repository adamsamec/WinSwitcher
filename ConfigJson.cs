namespace WinSwitcher
{
    public class ConfigJson
    {
        public Settings settings { get; set; }
    }

    public class Settings
    {
        public string launchOnStartup { get; set; }
        public string filterByTyping { get; set; }
        public Enabledshortcuts enabledShortcuts { get; set; }
    }

    public class Enabledshortcuts
    {
        public Showapps showApps { get; set; }
        public Showwindows showWindows { get; set; }
    }

    public class Showapps
    {
        public string Win_F12 { get; set; }
        public string Win_Shift_A { get; set; }
    }

    public class Showwindows
    {
        public string Win_F11 { get; set; }
        public string Win_Shift_W { get; set; }
    }
}
