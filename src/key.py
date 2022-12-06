import os
import sys

### Translate the specified virtual-key code and keyboard state
#   to the corresponding Unicode character or characters.
#   learn.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-tounicodeex
### Adapted from
#   the solution to https://stackoverflow.com/questions/38224277/
#   by https://stackoverflow.com/users/235698/mark-tolonen
###

from ctypes import (
    WinDLL, POINTER, create_string_buffer, create_unicode_buffer,
    c_int32, c_uint, c_uint, c_char, c_wchar, c_int, c_uint, c_void_p
    )
_ToUnicodeEx = WinDLL('user32').ToUnicodeEx
_ToUnicodeEx.argtypes = [
        c_uint,           # wVirtKey   virtual-key code to be translated
        c_uint,           # wScanCode  hardware scan code of ˙wVirtKey˙
        POINTER(c_char),  # lpKeyState current keyboard state (256-byte array)
        POINTER(c_wchar), # pwszBuff   buffer that receives translated chars
        c_int,            # cchBuff    size of the `pwszBuff` buffer (in chars)
        c_uint,           # wFlags     behavior of the function
        c_void_p          # dwhkl      input locale identifier
]
_ToUnicodeEx.restype = c_int


def ToUn(vk,sc,wfl,hkid, shiftDown=False):
    kst = create_string_buffer(256)
    if shiftDown:
        kst[16] = 0x80
    b = create_unicode_buffer(5)
    if _ToUnicodeEx(vk,sc,kst,b,5,wfl,hkid):
        return b.value
    else:
        return chr( 0xFFFD) # Replacement Character


### Retrieve the active input locale identifier
#   (formerly called the keyboard layout)
#   https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getkeyboardlayout
###
#   Method based on my own research; non-optimized, debugged on Windows 10… 
###

from ctypes import WinDLL
user32 = WinDLL('user32', use_last_error=True)

def get_servant_conhost(pid, proclist):
    """Find “attendant” host process (conhost.exe)"""
    aux = [_ for _ in proclist if _[0] == pid]
    if len( aux) > 0:
        auxcon = [x for x in proclist if (
                x[1] == aux[0][0] and x[2] == "conhost.exe")]
        if len( auxcon) == 0:
            auxconret = get_servant_conhost(aux[0][1], proclist)
            return auxconret
        else:
            auxconret = auxcon[0]
            auxconret.append( aux[0][2])
            return auxconret
    else:
        return []


def get_conhost_threads():
    if sys.executable.lower().endswith('\\pythonw.exe'):
        return []
    import wmi
    c = wmi.WMI()
    w_where = ' or '.join([
        'Name like "p%.exe"',  # py.exe|python.exe|pwsh.exe|powershell.exe 
        'Name = "conhost.exe"',
        'Name = "cmd.exe"'
    ])
    w_properties = 'ProcessId, ParentProcessId, Name'
    w_wql = f'SELECT {w_properties} FROM Win32_Process where {w_where}'
    w_wqlaux = c.query(w_wql)
    proc_list = [[wqlitem.__getattr__('ProcessId'),
          wqlitem.__getattr__('ParentProcessId'),
          wqlitem.__getattr__('Name')] for wqlitem in w_wqlaux] 
    servant_conhost = get_servant_conhost(os.getpid(), proc_list)
    if len( servant_conhost) == 0:
        return []
    else:
        try:
            w_where = f'ProcessHandle = {servant_conhost[0]}'
            w_wql = f'SELECT Handle FROM Win32_Thread WHERE {w_where}'
            w_wqlHandle = c.query(w_wql)
            wqlthreads = [x.__getattr__('Handle') for x in w_wqlHandle]
        except:
            wqlthreads = []
    return wqlthreads


# required if run from `cmd` or from the `Run` dialog box (`<WinKey>+R`) 
conhost_threads = get_conhost_threads()
                                    

def get_current_keyboard_layout():
    foregroundWindow  = user32.GetForegroundWindow();
    foregroundProcess = user32.GetWindowThreadProcessId(int(foregroundWindow), 0);
    keyboardLayout    = user32.GetKeyboardLayout(int(foregroundProcess));
    keyboardLayout0   = user32.GetKeyboardLayout(int(0));
    if keyboardLayout == 0  or len(conhost_threads):                 
        if keyboardLayout == 0:
            keyboardLayout = keyboardLayout0
        for thread in conhost_threads:
            aux = user32.GetKeyboardLayout( int(thread))
            if aux != 0 and aux != keyboardLayout0:
                keyboardLayout = aux
                break
    return keyboardLayout

def getLayoutKey(key, shiftDown):
    c_hkl = get_current_keyboard_layout()
    layoutKey = ToUn(key, 0, 0,c_hkl, shiftDown)
    return layoutKey
