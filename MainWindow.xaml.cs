using System.ComponentModel;
using System.Runtime.InteropServices;
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

        [DllImport("user32", EntryPoint = "GetWindowLong")]
        public static extern uint GetWindowLong(IntPtr hwnd, int nIndex);

        [DllImport("user32", EntryPoint = "SetWindowLong")]
        public static extern uint SetWindowLong(
        IntPtr hwnd,
        int nIndex,
        uint dwNewLong
        );

        public const int WS_EX_TOOLWINDOW = 0x00000080;
        public static readonly int GWL_EXSTYLE = -20;
        
        public MainWindow()
        {
            InitializeComponent();


            //ShowInTaskbar = false;

            _switcher = new Switcher(this);

            KeyDown += MainWindow_KeyDown;
            Closing += MainWindow_Closing;
        }

        private void SetWindowToolStyle(IntPtr hwnd)
        {
            uint extendedStyle = GetWindowLong(hwnd, GWL_EXSTYLE);
            SetWindowLong(hwnd, GWL_EXSTYLE, extendedStyle |
            WS_EX_TOOLWINDOW);
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
