using System.Collections.Generic;
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

            Closing += (sender, e) =>
            {
                _switcher.CleanUp();
            };
        }

        private void ItemsListBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                _switcher.SwitchToItem(itemsListBox.SelectedIndex);
            }
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            Hide();
            _switcher = new Switcher(this);
            itemsListBox.KeyDown += new KeyEventHandler(ItemsListBox_KeyDown);
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
            itemsList.ForEach(item => itemsListBox.Items.Add(item));
        }
    }
}
