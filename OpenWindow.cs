namespace WinSwitcher
{
    /// <summary>
    /// Class for storing open window information
    /// </summary>
    public class OpenWindow
    {
        public string Title { get; set; }
        public IntPtr Handle { get; set; }
        public uint Pid { get; set; }

        public OpenWindow(string title, IntPtr handle, uint pid)
        {
            Title = title;
            Handle = handle;
            Pid = pid;
        }

    }
}

