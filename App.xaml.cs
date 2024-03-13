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
        private const bool _useCzechByDefault = false;

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
                    var lang = _useCzechByDefault ? "cs-CZ" : "en-US"; 
                    WinSwitcher.Resources.Culture = new System.Globalization.CultureInfo(lang);
                    break;
            }


        }

    }

}
