using System.ComponentModel;
using System.Windows;
using System.Timers;
using System.Windows.Controls;
using System.Windows.Input;
using System.Windows.Interop;
using System.Diagnostics;
using System.Windows.Threading;

namespace WinSwitcher
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Switcher _switcher;
        private int _prevItemsListIndex = 0;

        public MainWindow()
        {
            InitializeComponent();

            _switcher = new Switcher(this);

            KeyDown += MainWindow_KeyDown;
            Closing += MainWindow_Closing;
        }

        private void SetWindowToolStyle(IntPtr handle)
        {
            uint extendedStyle = NativeMethods.GetWindowLong(handle, NativeMethods.GWL_EXSTYLE);
            NativeMethods.SetWindowLong(handle, NativeMethods.GWL_EXSTYLE, extendedStyle |
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
            switch (e.Key)
            {
                case Key.Enter:
                    _switcher.SwitchToItem(itemsListBox.SelectedIndex);
                    break;
                case Key.Back:
                    _switcher.ResetFilter();
                    break;
                case Key.Right:
                        _prevItemsListIndex = itemsListBox.SelectedIndex;
                    if (_switcher.ShowSelectedAppWindows(itemsListBox.SelectedIndex))
                    {
                        FocusItemAfterDelay(0);
                    }
                    break;
                case Key.Left:
                    if (_switcher.ShowApps())
                    {
                        FocusItemAfterDelay(_prevItemsListIndex);
                    }
                    break;
                default:
                    var character = e.Key.ToPrintableCharacter();
                    if (e.Key != Key.Tab && character != "")
                    {
                        _switcher.ApplyTypedCharacterToFilter(character);
                    }
                    break;
            }
        }

        public void SetListBoxLabel(string text)
        {
            llistboxLabel.Content = text;
        }

        public void Display()
        {
            Show();
            Activate();
            FocusItemAfterDelay(0);
        }

        private void FocusItemAfterDelay(int itemIndex)
        {
                        itemsListBox.SelectedIndex = itemIndex;
            var timer = new System.Windows.Threading.DispatcherTimer();
            timer.Tick += new EventHandler((sender, e) => {
                (sender as DispatcherTimer).Stop();
                ((ListBoxItem)itemsListBox.SelectedItem).Focus();
            });
            timer.Interval = TimeSpan.FromMilliseconds(100);
            timer.Start();
        }

    public void SetListBoxItems(List<string> itemsList)
        {
            itemsListBox.Items.Clear();
            if (itemsList.Count == 0)
            {
                var listBoxItem = new ListBoxItem();
                listBoxItem.Content = _switcher.View == Switcher.ListView.Apps ? WinSwitcher.Resources.noAppsFound : WinSwitcher.Resources.noWindowsFound;
                itemsListBox.Items.Add(listBoxItem);
                return;
            }
            foreach (var item in itemsList)
            {
                var listBoxItem = new ListBoxItem();
                listBoxItem.Content = item;
                itemsListBox.Items.Add(listBoxItem);
            }
        }
    }
}
