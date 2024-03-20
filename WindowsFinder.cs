using System.Text;

namespace WinSwitcher
{
    /// <summary>
    /// Class for getting the list of open windows
    /// </summary>
    public static class WindowsFinder
    {
        const int GWL_EXSTYLE = -20;
        const uint DWMWA_CLOAKED = 14;
        const uint DWM_CLOAKED_SHELL = 0x00000002;
        const uint GA_ROOTOWNER = 3;
        const uint WS_EX_TOOLWINDOW = 0x00000080;
        const uint WS_EX_TOPMOST = 0x00000008;
        const uint WS_EX_NOACTIVATE = 0x08000000;

        private static List<OpenWindow> _windows = new List<OpenWindow>();

        public static List<OpenWindow> GetOpenWindows()
        {
            _windows.Clear();
            NativeMethods.EnumWindows(GetAltTabWindows, IntPtr.Zero);
            NativeMethods.EnumChildWindows(NativeMethods.GetDesktopWindow(), GetFullScreenUWPWindows, IntPtr.Zero);
            return _windows;
        }

        private static void AddWindow(IntPtr handle)
        {
            var title = GetWindowTitle(handle);
            uint pid;
            NativeMethods.GetWindowThreadProcessId(handle, out pid);
            var window = new OpenWindow(title, handle, pid);
            _windows.Add(window);
        }

        public static string GetWindowTitle(IntPtr handle)
        {
            var length = NativeMethods.GetWindowTextLength(handle) + 1;
            var title = new StringBuilder(length);
            NativeMethods.GetWindowText(handle, title, length);
            return title.ToString();
        }

        private static bool GetAltTabWindows(IntPtr handle, IntPtr lparam)
        {
            if (IsAltTabWindow(handle))
            {
                AddWindow(handle);
            }

            return true;
        }

        private static int GetFullScreenUWPWindows(IntPtr handle, IntPtr lparam)
        {
            // Check only the windows whose class name is ApplicationFrameInputSinkWindow
            StringBuilder className = new StringBuilder(1024);
            NativeMethods.GetClassName(handle, className, className.Capacity);
            if (className.ToString() != "ApplicationFrameInputSinkWindow")
                return 0;

            // Get the root owner of the window
            IntPtr rootOwner = NativeMethods.GetAncestor(handle, GA_ROOTOWNER);

            if (IsFullScreenUWPWindows(rootOwner))
            {
                AddWindow(handle);
            }

            return 0;
        }

        private static bool IsAltTabWindow(IntPtr handle)
        {
            // The window must be visible
            if (!NativeMethods.IsWindowVisible(handle))
                return false;

            // The window must be a root owner
            if (NativeMethods.GetAncestor(handle, GA_ROOTOWNER) != handle)
                return false;

            // The window must not be cloaked by the shell
            NativeMethods.DwmGetWindowAttribute(handle, DWMWA_CLOAKED, out uint cloaked, sizeof(uint));
            if (cloaked == DWM_CLOAKED_SHELL)
                return false;

            // The window must not have the extended style WS_EX_TOOLWINDOW
            uint style = NativeMethods.GetWindowLong(handle, GWL_EXSTYLE);
            if ((style & WS_EX_TOOLWINDOW) != 0)
                return false;

            return true;
        }

        private static bool IsFullScreenUWPWindows(IntPtr handle)
        {
            // Get the extended style of the window
            uint style = NativeMethods.GetWindowLong(handle, GWL_EXSTYLE);

            // The window must have the extended style WS_EX_TOPMOST
            if ((style & WS_EX_TOPMOST) == 0)
                return false;

            // The window must not have the extended style WS_EX_NOACTIVATE
            if ((style & WS_EX_NOACTIVATE) != 0)
                return false;

            // The window must not have the extended style WS_EX_TOOLWINDOW
            if ((style & WS_EX_TOOLWINDOW) != 0)
                return false;

            return true;
        }

    }
}

