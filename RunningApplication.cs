using System.Diagnostics;

namespace WinSwitcher
{
    /// <summary>
    /// Class for storing running application information
    /// </summary>
    public class RunningApplication
    {
        private int _zIndex;

        public Process LastWindowProcess { get; set; }
        public string Name { get; set; }
        public int ZIndex
        {
            get
            {
                return _zIndex;
            }
        }

        public RunningApplication(Process lastWindowProcess, string name)
        {
            LastWindowProcess = lastWindowProcess;
            Name = name;

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

