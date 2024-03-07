using System.Configuration;
using System.Data;
using System.Windows;

namespace WinSwitcher
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);
            SetLanguageDictionary();
        }

        private void SetLanguageDictionary()
        {
            switch (Thread.CurrentThread.CurrentCulture.ToString())
            {
                case "cs-CZ":
                    WinSwitcher.Resources.Culture = new System.Globalization.CultureInfo("cs-CZ");
                    break;
                default:
                    WinSwitcher.Resources.Culture = new System.Globalization.CultureInfo("en-US");
                    break;
            }


        }

    }

}
