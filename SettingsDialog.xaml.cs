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
        public SettingsDialog()
        {
            InitializeComponent();
        }

        private void SettingsDialog_Loaded(object sender, RoutedEventArgs e)
        {
        }

        private void closeButton_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = true;
        }

        private void launchOnStartupCheckBox_Checked(object sender, RoutedEventArgs e)
        {

        }

        private void launchOnStartupCheckBox_Unchecked(object sender, RoutedEventArgs e)
        {

        }

    }
}