using AccessibleOutput;
using System.Diagnostics;
using System.IO;
using System.Media;
using System.Windows.Input;

namespace WinSwitcher
{
    /// <summary>
    /// Main application logic
    /// </summary>
    public class Switcher
    {
        private IntPtr _prevWindowHandle = NativeMethods.GetForegroundWindow();
        private MainWindow _mainWindow;
        private KeyboardHook _hook;
        private AutoOutput _srOutput;
        private Config _config;

        private List<RunningApplication> _appsList = new List<RunningApplication>();
        private List<RunningApplication> _filteredAppsList = new List<RunningApplication>();
        private string _filterText;

        public Switcher(MainWindow mainWindow)
        {
            _mainWindow = mainWindow;
            _config = new Config();
            _hook = new KeyboardHook(_mainWindow, 0x77, ModifierKeyCodes.Windows);
            _hook.Triggered += ShowApps;

            _srOutput = new AutoOutput();
            _srOutput.Speak(Resources.startAnnouncement);
        }

        public void HandleMainWindowLoad()
        {
            Hide();
        }

        public void HideAndSwitchToPrevWindow()
        {
            Hide();
            NativeMethods.SetForegroundWindow(_prevWindowHandle);
            NativeMethods.SetActiveWindow(_prevWindowHandle);
        }

        private void Hide()
        {
            _mainWindow.Hide();
        }

        private void ShowApps()
        {
            SystemSounds.Hand.Play();
            _prevWindowHandle = NativeMethods.GetForegroundWindow();

            // Update list of running applications
            var processes = Process.GetProcesses();
            _appsList.Clear();
            foreach (var process in processes)
            {
                if (String.IsNullOrEmpty(process.MainWindowTitle))
                {
                    continue;
                }
                string appName;
                try
                {
                    var fileVersionInfo = FileVersionInfo.GetVersionInfo(process.GetMainModuleFilePath());
                    appName = fileVersionInfo.FileDescription;
                    if (String.IsNullOrEmpty(appName))
                    {
                        continue;
                    }
                }
                catch (Exception ex)
                {
                    appName = process.MainWindowTitle;
                }
                var app = new RunningApplication(process, appName);
                _appsList.Add(app);
            }
            _appsList = _appsList.OrderBy(app => app.ZIndex).ToList();

            // Update filtred apps and set apps names list for main window
            _filteredAppsList.Clear();
            _filterText = "";
            var appsNamesList = new List<string>();
            foreach (var app in _appsList)
            {
                _filteredAppsList.Add(app);
                appsNamesList.Add(app.Name);
            }
            _mainWindow.SetItems(appsNamesList);

            // Display main window
            _mainWindow.Show(); // This extra Show() fixes the initial display
            _mainWindow.Display();
        }

        public void SwitchToApp(int itemNum)
        {
            // Ignore switching if there are no apps after applying filter
            if (_filteredAppsList.Count == 0)
            {
                return;
            }
            Hide();
            var process = _filteredAppsList[itemNum].LastWindowProcess;
            IntPtr handle = process.MainWindowHandle;
            NativeMethods.ShowWindow(handle, 5);
            NativeMethods.SetForegroundWindow(handle);
            NativeMethods.SetActiveWindow(handle);
        }

        public void ApplyTypedCharacterToFilter(string character)
        {
            if (_config.Settings.filterByTyping != Config.TRUE)
            {
                return;
            }
            character = character.ToLower();
            _filterText += character;
            _filteredAppsList.Clear();
            var appsNamesList = new List<string>();
            foreach (var app in _appsList)
            {
                if (app.Name.ToLower().Contains(_filterText))
                {
                _filteredAppsList.Add(app);
                    appsNamesList.Add(app.Name);
                }
                _mainWindow.SetItems(appsNamesList);
            }
        }

        public void ResetFilter()
        {
            _filteredAppsList.Clear();
            var appsNamesList = new List<string>();
            foreach (var app in _appsList)
            {
                _filteredAppsList.Add(app);
                appsNamesList.Add(app.Name);
            }
            if (appsNamesList.Count == 0)
            {
                //appsNamesList.Add(Resources.noAppsFound);
            }
            _mainWindow.SetItems(appsNamesList);
        }

        public void CleanUp()
        {
            _hook.Dispose();
        }
    }
}
