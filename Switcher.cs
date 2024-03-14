using AccessibleOutput;
using System.Diagnostics;
using System.Media;

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

        private Process _currentProcess = Process.GetCurrentProcess();
        private List<Process> _processesList = new List<Process>();

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
        }

        private void Hide()
        {
            _mainWindow.Hide();
        }

        private void ShowApps()
        {
            SystemSounds.Hand.Play();

            _prevWindowHandle = NativeMethods.GetForegroundWindow();

                    var processes = Process.GetProcesses();
                    var appTitlesList = new List<string>();
                    _processesList.Clear();
                    foreach (var process in processes)
                    {
                        if (!String.IsNullOrEmpty(process.MainWindowTitle))
                        {
                            appTitlesList.Add(process.MainWindowTitle);
                            _processesList.Add(process);
                        }
                    }

                    _mainWindow.SetItems(appTitlesList);
            _mainWindow.Show(); // This extra Show() fixes the initial display
            _mainWindow.Display();
        }

        public void SwitchToItem(int itemNum)
        {
            _mainWindow.Hide();
            var process = _processesList[itemNum];
            IntPtr handle = process.MainWindowHandle;
            NativeMethods.SetForegroundWindow(handle);
            NativeMethods.SetActiveWindow(handle);
        }

        public void CleanUp()
        {
            _hook.Dispose();
        }
    }
}
