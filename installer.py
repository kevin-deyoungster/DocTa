from subprocess import Popen, STDOUT, check_call

import os
import shutil
import platform
from config import data

from os import remove
from sys import argv


def create_desktop_shortcut(target_program, icon_path):
    try:
        import winshell
    except ImportError as e:
        print("Winshell package not installed. Installing winshell...")
        Popen(["pip", "install", "winshell"]).communicate()
    import winshell
    from win32com.client import Dispatch

    desktop = winshell.desktop()
    path = os.path.join(desktop, "DocTa.lnk")
    target = os.path.join(os.getcwd(), target_program)
    wDir = os.getcwd()
    icon = os.path.join(os.getcwd(), icon_path)

    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()


def install_python_modules(pip_version):
    if not shutil.which("python"):
        print("Python Not Installed")
    elif not shutil.which(pip_version):
        print("Pip Not Installed")
    else:
        Popen([pip_version, "install", "-r", "requirements.txt"]).communicate()
        print("Installed Python Packages!")


def install_linux_dependencies():
    dependencies = data.PATH_DEPENDENCIES_LINUX
    check_call(["sudo", "apt-get", "install", "-y"] + dependencies, stderr=STDOUT)


def self_destruct(retain_copy=True):
    shutil.copyfile(
        os.path.join(os.getcwd(), "installer.py"),
        os.path.join(os.getcwd(), "modules\\preserved\\installer.py"),
    )
    # remove(argv[0])


def _system_os_is(os):
    return platform.system().lower() == os


def install():
    if _system_os_is("windows"):
        create_desktop_shortcut("docta.py", "public/images/favicon.ico")
        install_python_modules("pip")
        self_destruct()
    elif _system_os_is("linux"):
        install_linux_dependencies()
        install_python_modules("pip 3")
    else:
        print("Current OS Not Supported")


install_linux_dependencies()
