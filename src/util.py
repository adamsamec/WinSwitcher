import win32gui
import win32process

# Utility class.
class Util:

  @staticmethod
  def getActiveWindowPid():
    pids = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
    return pids[-1]
