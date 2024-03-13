﻿using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Media;
using System.Runtime.InteropServices;
using System.Windows;

using AccessibleOutput;

namespace WinSwitcher
{
    /// <summary>
    /// Main application logic
    /// </summary>
    public class Switcher
    {
        private MainWindow _mainWindow;
        private KeyboardHook _hook;
        private AutoOutput _srOutput;
        private Config _config;
        private IntPtr _prevWindowHandle;

        private Process _currentProcess = Process.GetCurrentProcess();
        private List<Process> _processesList = new List<Process>();

        [DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();

        [DllImport("User32.dll")]
        private static extern bool SetForegroundWindow(IntPtr handle);

        [DllImport("User32.dll")]
        private static extern bool SetActiveWindow(IntPtr handle);

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
            SetForegroundWindow(_prevWindowHandle);
        }

        private void Hide()
        {
            _mainWindow.Hide();
            _mainWindow.WindowState = WindowState.Minimized;
        }

        private void ShowApps()
        {
            SystemSounds.Hand.Play();

            _prevWindowHandle = GetForegroundWindow();

                    var processes = Process.GetProcesses();
                    var appTitlesList = new List<string>();
                    _processesList.Clear();
                    foreach (var process in processes)
                    {
                        if (!String.IsNullOrEmpty(process.MainWindowTitle))
                        {
                            //appTitlesList.Add(process.MainWindowTitle);
                            appTitlesList.Add(process.ProcessName);
                            _processesList.Add(process);
                        }
                    }

                    _mainWindow.SetItems(appTitlesList);
            _mainWindow.WindowState = WindowState.Normal;
                    _mainWindow.Display();
        }

        public void SwitchToItem(int itemNum)
        {
            _mainWindow.Hide();
            var process = _processesList[itemNum];
            IntPtr handle = process.MainWindowHandle;
            SetForegroundWindow(handle);
            SetActiveWindow(handle);
        }

        public void CleanUp()
        {
            _hook.Dispose();
        }
    }
}
