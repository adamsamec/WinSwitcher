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

        private Process _currentProcess = Process.GetCurrentProcess();
        private List<Process> _processesList = new List<Process>();

        [DllImport("User32.dll")]
        private static extern bool SetForegroundWindow(IntPtr handle);

        [DllImport("User32.dll")]
        private static extern bool SetActiveWindow(IntPtr handle);

        public Switcher(MainWindow mainWindow)
        {
            _mainWindow = mainWindow;
            _config = new Config();
            _config.Load();
            _hook = new KeyboardHook(_mainWindow, 0x77, ModifierKeyCodes.Windows);
            _hook.Triggered += ShowApps;

            _srOutput = new AutoOutput();
            _srOutput.Speak(Resources.startAnnouncement);
        }

        private void ShowApps()
        {
            SystemSounds.Hand.Play();

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
        }

        public void SwitchToItem(int itemNum)
        {
            _mainWindow.Hide();
            Process process = _processesList[itemNum];
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
