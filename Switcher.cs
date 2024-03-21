using AccessibleOutput;
using System.Diagnostics;
using System.Media;
using System.Speech.Synthesis.TtsEngine;
using System.Windows.Markup.Localizer;

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
        private List<OpenWindow> _filteredWindowsList = new List<OpenWindow>();
        private string _appsOrWindowsFilterText;
        private string _SelectedAppWindowsFilterText;
        private int _selectedAppIndex = 0;
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

            // Determine and update ListBox items
            var appsItemsList = new List<string>();
            foreach (var app in _filteredAppsList)
            {
                appsItemsList.Add(GetAppItemText(app));
            }
            _mainWindow.SetListBoxItems(appsItemsList);

            return true;
        }

        public static string GetAppItemText(RunningApplication app)
        {
                var itemText = $"{app.Name} ({app.Windows.Count} {Resources.windowsCount})";
            return itemText;
        }

        public bool ShowSelectedAppWindows(int appIndex)
        {
            if (View != ListView.Apps || _filteredAppsList.Count == 0)
            {
                return false;
            }

            // Determine selected app and its windows
            _filteredWindowsList.Clear();
            _SelectedAppWindowsFilterText = "";
            _selectedAppIndex = appIndex;
            var windows = _filteredAppsList[appIndex].Windows;
            foreach (var window in windows)
            {
                _filteredWindowsList.Add(window);
            }
            _view = ListView.SelectedAppWindows;

            // Determine and update ListBox items
            var windowsTitlesList = new List<string>();
            foreach (var window in _filteredWindowsList)
            {
                windowsTitlesList.Add(window.Title);
            }
            _mainWindow.SetListBoxItems(windowsTitlesList);

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
                    var process = processApp.AppProcess;
                    if (app.AppProcess.ProcessName == process.ProcessName)
                    {
                        appExists = true;
                        var handle = process.Handle;
                        uint pid;
                        NativeMethods.GetWindowThreadProcessId(handle, out pid);
                        var window = new OpenWindow(process.MainWindowTitle, handle, pid);
                        app.Windows.Add(window);
                    }
                }
                if (!appExists)
                {
                    _appsList.Add(processApp);
                }
            }

            // Update filtred apps list
            _filteredAppsList.Clear();
            _appsOrWindowsFilterText = "";
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
                    if (window.Pid == app.AppProcess.Id)
                    {
                        app.Windows.Add(window);
                    }
                }
            }
        }

        public void SwitchToItem(int itemIndex)
        {
            // Ignore switching if there are no items after applying filter
            if (View == ListView.Apps && _filteredAppsList.Count == 0)
            {
                return;
            }
            if ((View == ListView.FrontAppWindows || View == ListView.SelectedAppWindows) && _filteredWindowsList.Count == 0)
            {
                return;
            }

            // Determine window handle to switch to
            IntPtr handle = -1;
            switch (View)
            {
                case ListView.Apps:
            var process = _filteredAppsList[itemIndex].AppProcess;
            handle = process.MainWindowHandle;
                    break;
                case ListView.SelectedAppWindows:
                    handle = _filteredWindowsList[itemIndex].Handle;
                    break;
            }
            if (handle == -1)
            {
                return;
            }

            // Hide switcher and switch to app or window using handle
                Hide();
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
            var itemsTextsList = new List<string>();
            switch (View)
            {
                case ListView.Apps:
                    _appsOrWindowsFilterText += character;
                    _filteredAppsList.Clear();
                    foreach (var app in _appsList)
                    {
                        if (app.Name.ToLower().Contains(_appsOrWindowsFilterText))
                        {
                            _filteredAppsList.Add(app);
                            itemsTextsList.Add(GetAppItemText(app));
                        }
                    }
                    break;
                case ListView.SelectedAppWindows:
                    _SelectedAppWindowsFilterText += character;
                    _filteredWindowsList.Clear();
                    var windows = _filteredAppsList[_selectedAppIndex].Windows;
                    foreach (var window in windows)
                    {
                        if (window.Title.ToLower().Contains(_SelectedAppWindowsFilterText))
                        {
                            _filteredWindowsList.Add(window);
                            itemsTextsList.Add(window.Title);
                        }
                    }
                    break;
            }

                _mainWindow.SetListBoxItems(itemsTextsList);
        }

        public void ResetFilter()
        {
                    var itemsTextsList = new List<string>();
            switch (View)
            {
                case ListView.Apps:
                    _filteredAppsList.Clear();
                    foreach (var app in _appsList)
                    {
                        _filteredAppsList.Add(app);
                        itemsTextsList.Add(GetAppItemText(app));
                    }
            break;
                case ListView.SelectedAppWindows:
                    _filteredWindowsList.Clear();
                    var windows = _filteredAppsList[_selectedAppIndex].Windows;
                    foreach (var window in windows)
                    {
                        _filteredWindowsList.Add(window);
                        itemsTextsList.Add(window.Title);
                    }
                    break;
            }

            _mainWindow.SetListBoxItems(itemsTextsList);
        }

        public void CleanUp()
        {
            _hook.Dispose();
        }
    }
}
