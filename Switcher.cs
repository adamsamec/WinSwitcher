using AccessibleOutput;
using System;
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
        private ListView _view = ListView.Hidden;

        public ListView View
        {
            get { return _view; }
        }

        public enum ListView
        {
            Hidden,
            Apps,
            SelectedAppWindows,
            FrontAppWindows
        }

        public Switcher(MainWindow mainWindow)
        {
            _mainWindow = mainWindow;
            _config = new Config();
            _hook = new KeyboardHook(_mainWindow, 0x77, ModifierKeyCodes.Windows);
            _hook.Triggered += Show;

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

        private void Show()
        {
            SystemSounds.Hand.Play();
            _prevWindowHandle = NativeMethods.GetForegroundWindow();
            UpdateApps();
            UpdateWindows();
            ShowApps();

            // Display main window
            _mainWindow.Show(); // This extra Show() fixes the initial display
            _mainWindow.Display();
        }

        public bool ShowApps()
        {
            if (View != ListView.Hidden && View != ListView.SelectedAppWindows)
            {
                return false;
            }
            _view = ListView.Apps;
            var appsItemsList = new List<string>();
            foreach (var app in _filteredAppsList)
            {
                var itemText = $"{app.Name} ({app.Windows.Count} {Resources.windowsCount})";
                appsItemsList.Add(itemText);
            }
            _mainWindow.SetItems(appsItemsList);
            return true;
        }

        public bool ShowSelectedAppWindows(int appNum)
        {
            if (View != ListView.Apps)
            {
                return false;
            }
            if (_filteredAppsList.Count == 0)
            {
                return false;
            }
            _view = ListView.SelectedAppWindows;
            var app = _filteredAppsList[appNum];
            var windowsTitlesList = new List<string>();
            foreach (var window in app.Windows)
            {
                windowsTitlesList.Add(window.Title);
            }
            _mainWindow.SetItems(windowsTitlesList);
            return true;
        }

        private void UpdateApps()
        {
            var processes = Process.GetProcesses();
            var processesAppsList = new List<RunningApplication>();
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

                var app = new RunningApplication(appName, process);
                processesAppsList.Add(app);
            }
            processesAppsList = processesAppsList.OrderBy(app => app.ZIndex).ToList();

            // Turn apps with the same process name into windows
            _appsList.Clear();
            foreach (var processApp in processesAppsList)
            {
                var appExists = false;
                foreach (var app in _appsList)
                {
                    var process = app.LastWindowProcess;
                    if (processApp.LastWindowProcess.ProcessName == process.ProcessName)
                    {
                        appExists = true;
                        var handle = process.Handle;
                        uint pid;
                        NativeMethods.GetWindowThreadProcessId(handle, out pid);
                        var window = new OpenWindow(process.MainWindowTitle, handle, pid);
                    }
                }
                if (!appExists)
                {
                    _appsList.Add(processApp);
            }
        }

            // Update filtred apps list
            _filteredAppsList.Clear();
            _filterText = "";
            foreach (var app in _appsList)
            {
                _filteredAppsList.Add(app);
            }
        }

        private void UpdateWindows()
        {
            var windows = WindowsFinder.GetWindows();
            foreach (var window in windows)
            {
                foreach (var app in _filteredAppsList)
                {
                    if (window.Pid == app.LastWindowProcess.Id)
                    {
                        app.Windows.Add(window);
                    }
                }
            }
        }

        public void SwitchToItem(int itemNum)
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
