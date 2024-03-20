using System.Runtime.InteropServices;
using System.Text;
using System.Windows;

namespace WinSwitcher
{
    /// <summary>
    /// Class for Win32 native methods access
    /// </summary>
    public static class NativeMethods
    {
        [DllImport("user32", EntryPoint = "GetWindowLong")]
        public static extern uint GetWindowLong(IntPtr handle, int nIndex);

        [DllImport("user32", EntryPoint = "SetWindowLong")]
        public static extern uint SetWindowLong(
        IntPtr handle,
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

        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr GetWindow(IntPtr handle, int nIndex);

        [DllImport("user32.dll")]
        public static extern bool ShowWindow(IntPtr handle, uint nCmdShow);

        [DllImport("Kernel32.dll")]
        public static extern bool QueryFullProcessImageName([In] IntPtr hProcess, [In] uint dwFlags, [Out] StringBuilder lpExeName, [In, Out] ref uint lpdwSize);

        [DllImport("user32.dll")]
        public static extern int ToUnicode(
    uint wVirtKey,
    uint wScanCode,
    byte[] lpKeyState,
    [Out, MarshalAs( UnmanagedType.LPWStr, SizeParamIndex = 4 )]
        StringBuilder pwszBuff,
    int cchBuff,
    uint wFlags);

        [DllImport("user32.dll")]
        public static extern bool GetKeyboardState(byte[] lpKeyState);

        [DllImport("user32.dll")]
        public static extern uint MapVirtualKey(uint uCode, Utils.MapType uMapType);

        public delegate bool EnumWindowsProc(IntPtr handle, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern bool EnumWindows(EnumWindowsProc enumProc, IntPtr lParam);

        public delegate int WindowEnumProc(IntPtr handle, IntPtr lparam);

        [DllImport("user32.dll")]
        public static extern bool EnumChildWindows(IntPtr handle, WindowEnumProc callback, IntPtr lParam);

        [DllImport("user32.dll")]
        public static extern IntPtr GetDesktopWindow();

        [DllImport("user32.dll")]
        public static extern int GetClassName(IntPtr handle, StringBuilder lpClassName, int nMaxCount);

        [DllImport("user32.dll")]
        public static extern IntPtr GetAncestor(IntPtr handle, uint gaFlags);

        [DllImport("user32.dll")]
        public static extern bool IsWindowVisible(IntPtr handle);

        [DllImport("dwmapi.dll")]
        public static extern int DwmGetWindowAttribute(IntPtr handle, uint dwAttribute, out uint pvAttribute, int cbAttribute);

        [DllImport("user32.dll")]
        public static extern int GetWindowTextLength(IntPtr handle);

        [DllImport("user32.dll")]
        public static extern int GetWindowText(IntPtr handle, StringBuilder lpString, int nMaxCount);

        [DllImport("user32.dll")]
        public static extern uint GetWindowThreadProcessId(IntPtr handle, out uint processId);
    }
}
