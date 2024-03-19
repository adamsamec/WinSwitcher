using System.Diagnostics;
using System.Text;
using System.Windows.Input;

namespace WinSwitcher
{
    /// <summary>
    /// Utility class
    /// </summary>
    public static class Utils
    {
        private static object GetPropValue(object obj, string propName)
        {
            return obj.GetType().GetProperty(propName).GetValue(obj, null);
        }

        private static void SetPropValue(object obj, string propName, object propValue)
        {
            obj.GetType().GetProperty(propName).SetValue(obj, propValue, null);
        }

        public static void SetYesOrNo(object obj, object defaultObj, string[] propNames)
        {
            foreach (string propName in propNames)
            {
                string propValue = (string)GetPropValue(obj, propName);
                string defaultPropValue = (string)GetPropValue(defaultObj, propName);
                string newPropValue = (propValue == "yes" || propValue == "no") ? propValue : defaultPropValue;
                SetPropValue(obj, propName, newPropValue);
            }
        }

        public enum MapType : uint
        {
            MAPVK_VK_TO_VSC = 0x0,
            MAPVK_VSC_TO_VK = 0x1,
            MAPVK_VK_TO_CHAR = 0x2,
            MAPVK_VSC_TO_VK_EX = 0x3,
        }

    }

    internal static class Extensions
    {
        public static string GetMainModuleFilePath(this Process process, int buffer = 1024)
        {
            var filePathBuilder = new StringBuilder(buffer);
            uint bufferLength = (uint)filePathBuilder.Capacity + 1;
            return NativeMethods.QueryFullProcessImageName(process.Handle, 0, filePathBuilder, ref bufferLength) ?
                filePathBuilder.ToString() :
                null;
        }

        public static string ToPrintableCharacter(this Key key)
        {
            string character = "";

            // Consider Backspace as non-printable character
            if (key == Key.Back)
            {
                return character;
            }

            int virtualKey = KeyInterop.VirtualKeyFromKey(key);
            var keyboardState = new byte[256];
            NativeMethods.GetKeyboardState(keyboardState);

            uint scanCode = NativeMethods.MapVirtualKey((uint)virtualKey, Utils.MapType.MAPVK_VK_TO_VSC);
            var stringBuilder = new StringBuilder(2);

            int result = NativeMethods.ToUnicode((uint)virtualKey, scanCode, keyboardState, stringBuilder, stringBuilder.Capacity, 0);
            switch (result)
            {
                case -1:
                    break;
                case 0:
                    break;
                default:
                    {
                        character = stringBuilder[0].ToString();
                        break;
                    }
            }
            return character;
        }

    }
}
