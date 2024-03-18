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

            // Update the list of running applications
            var processes = Process.GetProcesses();
            _appsList.Clear();
            foreach (var process in processes)
            {
                if (String.IsNullOrEmpty(process.MainWindowTitle))
                {
                    continue;
                }
                String appName;
                try
                {
                    var fileVersionInfo = FileVersionInfo.GetVersionInfo(process.GetMainModuleFilePath());
                    appName = fileVersionInfo.FileDescription;
                    if (String.IsNullOrEmpty(appName))
                    {
                        continue;
                    }
                }
                catch (FileNotFoundException ex)
                {
                    appName = process.MainWindowTitle;
                }
                var app = new RunningApplication(process, appName);
                _appsList.Add(app);
            }
            _appsList = _appsList.OrderBy(app => app.ZIndex).ToList();

            // Create applications names list
            var appsNamesList = new List<string>();
            foreach (var app in _appsList)
            {
                appsNamesList.Add(app.Name);
            }

            // Update and show the window
            _mainWindow.SetItems(appsNamesList);
            _mainWindow.Show(); // This extra Show() fixes the initial display
            _mainWindow.Display();
        }

        public void SwitchToApp(int itemNum)
        {
            Hide();
            var process = _appsList[itemNum].LastWindowProcess;
            IntPtr handle = process.MainWindowHandle;
            NativeMethods.ShowWindow(handle, 5);
            NativeMethods.SetForegroundWindow(handle);
            NativeMethods.SetActiveWindow(handle);
        }

        public void HandleFilterAddChar(char character)
        {
            if (_config.Settings.filterByTyping != Config.TRUE)
            {
                return;
            }
            var filteredAppsList = new List<RunningApplication>();
            foreach (var (item, index) in _appsList.Select((item, index) => (item, index)))
            {
                filteredAppsList.Add(item);
            }
        }

        public void CleanUp()
        {
            _hook.Dispose();
        }
    }
}
