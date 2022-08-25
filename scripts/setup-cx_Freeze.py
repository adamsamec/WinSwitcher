import cx_Freeze
import setup

options = {"build_exe": "..\\build\\WinSwitcher"}
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
    options={"build_exe": options},
    executables=executables,
)
