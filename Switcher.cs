using System.Diagnostics;
using System.Windows;
using System.Collections.Generic;

using NonInvasiveKeyboardHookLibrary;

namespace WinSwitcher
{
    /// <summary>
    /// Main application logic
    /// </summary>
    public class Switcher
    {
        private MainWindow _mainWindow;
        private static KeyboardHookManager _hook;

        private static KeyboardHookManager Hook => _hook ?? (_hook = new KeyboardHookManager());

        public Switcher(MainWindow mainWindow)
        {
            _mainWindow = mainWindow;

            InitKeyboardHook();
        }

        private void InitKeyboardHook()
        {
            Hook.Start();
            Hook.RegisterHotkey(NonInvasiveKeyboardHookLibrary.ModifierKeys.Control, 0x20, () => {
                Application.Current.Dispatcher.Invoke(delegate
                {
                    Process[] processes = Process.GetProcesses();
                    List<string> appsList = new List<string>();
                    foreach (Process process in processes)
                    {
                        if (!String.IsNullOrEmpty(process.MainWindowTitle))
                        {
                            appsList.Add(process.MainWindowTitle);
                        }
                    }

                    _mainWindow.SetItems(appsList);
                    _mainWindow.Display();
                });
            });
        }

        public void CleanUp()
        {
            Hook.UnregisterAll();
            Hook.Stop();
        }
    }
}
