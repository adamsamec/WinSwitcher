import ctypes
import gettext
import locale

SUPPORTED_LANGS = ['cs', 'en', 'sk']
DEFAULT_LANG = 'en'

# Detect and save the system UI language
windll = ctypes.windll.kernel32
lang = locale.windows_locale[windll.GetUserDefaultUILanguage()].split('_')[0]
if not lang in SUPPORTED_LANGS:
  lang = DEFAULT_LANG

# Determine the gettext function for the detected language
trans = gettext.translation('base', localedir='locales', languages=[lang])
trans.install()

_ = trans.gettext
ngettext = trans.ngettext
