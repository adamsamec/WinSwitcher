using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;

namespace WinSwitcher
{
    /// <summary>
    /// Interaction logic for SettingsDialog.xaml
    /// </summary>
    public partial class SettingsDialog : Window
    {
        private Switcher _switcher;

        public SettingsDialog(Switcher switcher)
        {
        InitializeComponent();

            _switcher = switcher;
        }

        private void SettingsDialog_Loaded(object sender, RoutedEventArgs e)
        {
            // Retrieve stored settings
            launchOnStartupCheckBox.IsChecked = _switcher.Settings.launchOnStartup == Config.TRUE;

            launchOnStartupCheckBox.Focus();
        }

        private void closeButton_Click(object sender, RoutedEventArgs e)
        {
            _switcher.SaveSettings();
            DialogResult = true;
        }

        private void launchOnStartupCheckBox_Checked(object sender, RoutedEventArgs e)
        {
            _switcher.Settings.launchOnStartup = Config.TRUE;
        }

        private void launchOnStartupCheckBox_Unchecked(object sender, RoutedEventArgs e)
        {
            _switcher.Settings.launchOnStartup = Config.FALSE;
        }

    }
}