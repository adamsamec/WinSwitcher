using System.Collections.Generic;
using System.ComponentModel;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WinSwitcher
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Switcher _switcher;

        public MainWindow()
        {
            InitializeComponent();

            // Hack enabling hiding of the main window
/*
            var hiddenWindow = new Window();
            hiddenWindow.ShowInTaskbar = false;
            hiddenWindow.WindowStyle = WindowStyle.ToolWindow;
            hiddenWindow.Show();
            Owner = hiddenWindow;
            hiddenWindow.Hide();
*/
            ShowInTaskbar = false;

            _switcher = new Switcher(this);

            KeyDown += MainWindow_KeyDown;
            Closing += MainWindow_Closing;
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            _switcher.HandleMainWindowLoad();
            itemsListBox.KeyDown += new KeyEventHandler(ItemsListBox_KeyDown);
        }

        private void MainWindow_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Escape)
            {
                _switcher.HideAndSwitchToPrevWindow();
            }
        }

        private void MainWindow_Closing(object sender, CancelEventArgs e)
{
            _switcher.CleanUp();
        }

        private void ItemsListBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                _switcher.SwitchToItem(itemsListBox.SelectedIndex);
            }
        }

        public void Display()
        {
            Show();
            Activate();
            itemsListBox.Focus();
        }

        public void SetItems(List<string> itemsList)
        {
            itemsListBox.Items.Clear();
            foreach (var item in itemsList)
            {
                itemsListBox.Items.Add(item);
            }
        }
    }
}
