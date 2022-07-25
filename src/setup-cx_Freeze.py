import cx_Freeze

options = {
  'build_exe': '..\\build\\WinSwitcher'
}
executables = [cx_Freeze.Executable('WinSwitcher.py',
  # base = 'Win32GUI',
  targetName = 'WinSwitcher.exe'
  )]

cx_Freeze.setup(name = 'WinSwitcher' ,
  version = '0.1' ,
  description = '',
  options = {'build_exe': options},
  executables = executables
  )
