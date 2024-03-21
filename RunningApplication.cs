using System.Diagnostics;

namespace WinSwitcher
{
    /// <summary>
    /// Class for storing running application information
    /// </summary>
    public class RunningApplication
    {
        private int _zIndex;

        public string Name { get; set; }
        public Process LastWindowProcess { get; set; }
        public List<OpenWindow> Windows { get; set; }
        public int ZIndex
        {
            get { return _zIndex; }
        }

        public RunningApplication(string name, Process lastWindowProcess)
        {
            Name = name;
            LastWindowProcess = lastWindowProcess;
            Windows = new List<OpenWindow>();

            SetZOrder();
        }

        public void SetZOrder()
        {
            IntPtr handle = LastWindowProcess.MainWindowHandle;
            var z = 0;
            // 3 is GetWindowType.GW_HWNDPREV
            for (var h = handle; h != IntPtr.Zero; h = NativeMethods.GetWindow(h, 3))
            {
                z++;
            }
            _zIndex = z;
        }
    }
}

