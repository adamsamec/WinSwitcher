using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text;

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
    }
}

internal static class Extensions
{
    [DllImport("Kernel32.dll")]
    private static extern bool QueryFullProcessImageName([In] IntPtr hProcess, [In] uint dwFlags, [Out] StringBuilder lpExeName, [In, Out] ref uint lpdwSize);

    public static string GetMainModuleFilePath(this Process process, int buffer = 1024)
    {
        var filePathBuilder = new StringBuilder(buffer);
        uint bufferLength = (uint)filePathBuilder.Capacity + 1;
        return QueryFullProcessImageName(process.Handle, 0, filePathBuilder, ref bufferLength) ?
            filePathBuilder.ToString() :
            null;
    }
}