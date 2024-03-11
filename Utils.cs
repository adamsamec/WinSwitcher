using System.ComponentModel;

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
                string propValue = (string) GetPropValue(obj, propName);
                string defaultPropValue = (string)GetPropValue(defaultObj, propName);
                string newPropValue = (propValue == "yes" || propValue == "no") ? propValue : defaultPropValue;
                SetPropValue(obj, propName, newPropValue);
            }
        }

    }
}

