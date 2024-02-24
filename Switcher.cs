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

        private const NonInvasiveKeyboardHookLibrary.ModifierKeys _appsShortcutModifier = NonInvasiveKeyboardHookLibrary.ModifierKeys.WindowsKey;
        private const int _appsShortcutKey = 0x77; // F8
        
        private static KeyboardHookManager Hook => _hook ?? (_hook = new KeyboardHookManager());

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
                    Hook.Stop();

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
                Hook.Start();
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
