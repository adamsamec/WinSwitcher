namespace WinSwitcher
{ 
public class ConfigJson
{
    public Settings settings { get; set; }
}

public class Settings
{
    public bool launchOnStartup { get; set; }
    public bool filterByTyping { get; set; }
    public Enabledshortcuts enabledShortcuts { get; set; }
}

public class Enabledshortcuts
{
    public Showapps showApps { get; set; }
    public Showwindows showWindows { get; set; }
}

public class Showapps
{
    public bool WinShiftA { get; set; }
    public bool WinF12 { get; set; }
}

public class Showwindows
{
    public bool WinShiftW { get; set; }
    public bool WinF11 { get; set; }
}
}
