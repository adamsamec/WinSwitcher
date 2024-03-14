using System.Runtime.InteropServices;

namespace WinSwitcher
{
    /// <summary>
    /// Class for Win32 native methods access
    /// </summary>
    public static class NativeMethods
    {
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

        [DllImport("user32.dll")]
        public static extern IntPtr GetForegroundWindow();

        [DllImport("User32.dll")]
        public static extern bool SetForegroundWindow(IntPtr handle);

        [DllImport("User32.dll")]
        public static extern bool SetActiveWindow(IntPtr handle);
    }
}
