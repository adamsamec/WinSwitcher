import cx_Freeze
import setup

shortcut_table = [
    (
        "StartupShortcut",  # Shortcut
        "StartupFolder",  # Directory
        "WinSwitcher",  # Name
        "TARGETDIR",  # Component
        "[TARGETDIR]WinSwitcher.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
    (
        "DesktopShortcut",  # Shortcut
        "DesktopFolder",  # Directory
        "WinSwitcher",  # Name
        "TARGETDIR",  # Component
        "[TARGETDIR]WinSwitcher.exe",  # Target
        None,  # Arguments
        None,  # Description
        None,  # Hotkey
        None,  # Icon
        None,  # IconIndex
        None,  # ShowCmd
        "TARGETDIR",  # WkDir
    ),
]
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {
  "data": msi_data,
  "summary_data": {
    "author": setup.author,
  }
  }

options = {
    "include_files": [
        "..\\src\\locales",
        "..\\src\\config.default.json",
    ],
}
executables = [
    cx_Freeze.Executable(
        setup.main_path, base="Win32GUI", targetName=setup.target
    )
]

cx_Freeze.setup(
    name=setup.name,
    version=setup.version,
    description=setup.description,
    author=setup.author,
    author_email=setup.author_email,
    options={
        "bdist_msi": bdist_msi_options,
        "build_exe": options,
    },
    executables=executables,
)
