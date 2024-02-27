using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Media;
using System.Runtime.InteropServices;
using System.Windows;

using NonInvasiveKeyboardHookLibrary;

namespace WinSwitcher
{
    /// <summary>
    /// Main application logic
    /// </summary>
    public class Switcher
    {
        private Process _currentProcess = Process.GetCurrentProcess();
        private MainWindow _mainWindow;
        private static KeyboardHookManager _hook;
        private List<Process> _processesList = new List<Process>();

        private const NonInvasiveKeyboardHookLibrary.ModifierKeys _appsShortcutModifier = NonInvasiveKeyboardHookLibrary.ModifierKeys.WindowsKey | NonInvasiveKeyboardHookLibrary.ModifierKeys.Shift;
        private const int _appsShortcutKey = 0x41; // Letter "A"
        
        private static KeyboardHookManager Hook => _hook ?? (_hook = new KeyboardHookManager());

        [DllImport("User32.dll")]
        private static extern bool SetForegroundWindow(IntPtr handle);

        [DllImport("User32.dll")]
        private static extern bool SetActiveWindow(IntPtr handle);

        public Switcher(MainWindow mainWindow)
        {
            _mainWindow = mainWindow;

            InitKeyboardHook();
        }

        private void InitKeyboardHook()
        {
            Hook.Start();
            Hook.RegisterHotkey(_appsShortcutModifier, _appsShortcutKey, () => {
                Application.Current.Dispatcher.Invoke(delegate
                {
                    SystemSounds.Beep.Play();
                    Hook.Stop();

                    Process[] processes = Process.GetProcesses();
                    List<string> appTitlesList = new List<string>();
                    List<Process> processesList = new List<Process>();
                    _processesList.Clear();
                    foreach (Process process in processes)
                    {
                        if (!String.IsNullOrEmpty(process.MainWindowTitle))
                        {
                            appTitlesList.Add(process.MainWindowTitle);
                            _processesList.Add(process);
                        }
                    }

                    _mainWindow.SetItems(appTitlesList);
                    _mainWindow.Display();
                Hook.Start();
                });
            });
        }

        public void SwitchToItem(int itemNum)
        {
            Process process = _processesList[itemNum];
            IntPtr handle = process.MainWindowHandle;
            SetForegroundWindow(handle);
            SetActiveWindow(handle);
        }

        public void CleanUp()
        {
            Hook.UnregisterAll();
            Hook.Stop();
        }
    }
}
