﻿using System.Configuration;
using System.Data;
using System.Runtime.InteropServices;
using System.Windows;

namespace WinSwitcher
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private const bool _useCzechByDefault = false;

        public static IntPtr PrevWindowHandle = GetForegroundWindow();

        [DllImport("user32.dll")]
        private static extern IntPtr GetForegroundWindow();

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            SetLanguageDictionary();

            var mainWindow = new MainWindow();
        }

        private void SetLanguageDictionary()
        {
            switch (Thread.CurrentThread.CurrentCulture.ToString())
            {
                case "cs-CZ":
                    WinSwitcher.Resources.Culture = new System.Globalization.CultureInfo("cs-CZ");
                    break;
                default:
                    var lang = _useCzechByDefault ? "cs-CZ" : "en-US";
                    WinSwitcher.Resources.Culture = new System.Globalization.CultureInfo(lang);
                    break;
            }


        }

    }

}
