using System.ComponentModel;
using System.Windows;
using System.Windows.Input;
using System.Windows.Interop;

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

            _switcher = new Switcher(this);

            KeyDown += MainWindow_KeyDown;
            Closing += MainWindow_Closing;
        }

        private void SetWindowToolStyle(IntPtr hwnd)
        {
            uint extendedStyle = NativeMethods.GetWindowLong(hwnd, NativeMethods.GWL_EXSTYLE);
            NativeMethods.SetWindowLong(hwnd, NativeMethods.GWL_EXSTYLE, extendedStyle |
            NativeMethods.WS_EX_TOOLWINDOW);
        }

        private void MainWindow_Loaded(object sender, RoutedEventArgs e)
        {
            // Hide window from task switching
            SetWindowToolStyle(new WindowInteropHelper(this).Handle);

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
