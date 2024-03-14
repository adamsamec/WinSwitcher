using System.Runtime.InteropServices;
using System.Windows;
using System.Windows.Interop;

[Flags]
public enum ModifierKeyCodes : uint
{
    Alt = 1,
    Control = 2,
    Shift = 4,
    Windows = 8
}

/// <summary>
/// Virtual Key Codes
/// </summary>

class KeyboardHook : IDisposable
{
    [DllImport("user32.dll")]
    public static extern bool UnregisterHotKey(IntPtr hWnd, int id);

    [DllImport("user32.dll")]
    public static extern bool RegisterHotKey(IntPtr hWnd, int id, ModifierKeyCodes fdModifiers, int vk);

    #region Fields
    WindowInteropHelper host;
    bool IsDisposed = false;
    int Identifier;

    public Window Window { get; private set; }

    public int Key { get; private set; }

    public ModifierKeyCodes Modifiers { get; private set; }
    #endregion

    public KeyboardHook(Window Window, int Key, ModifierKeyCodes Modifiers)
    {
        this.Key = Key;
        this.Modifiers = Modifiers;

        this.Window = Window;
        host = new WindowInteropHelper(Window);

        Identifier = Window.GetHashCode();

        RegisterHotKey(host.Handle, Identifier, Modifiers, Key);

        ComponentDispatcher.ThreadPreprocessMessage += ProcessMessage;
    }

    void ProcessMessage(ref MSG msg, ref bool handled)
    {
        if ((msg.message == 786) && (msg.wParam.ToInt32() == Identifier) && (Triggered != null))
            Triggered();
    }

    public event Action? Triggered;

    public void Dispose()
    {
        if (!IsDisposed)
        {
            ComponentDispatcher.ThreadPreprocessMessage -= ProcessMessage;

            UnregisterHotKey(host.Handle, Identifier);
        }
        IsDisposed = true;
    }
}
