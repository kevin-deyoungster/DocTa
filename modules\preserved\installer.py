
from subprocess import Popen


import os
import shutil
import platform
import webbrowser

from os import remove
from sys import argv

# For Linux
from subprocess import STDOUT, check_call
from config import data


def create_desktop_shortcut(target_program, icon_path):
    from win32com.client import Dispatch

    try:
        import winshell
    except ImportError as e:
        print("Winshell package not installed. Installing winshell...")
        Popen(["pip", "install", "winshell"]).communicate()
    import winshell

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
    elif not shutil.which("pip"):
        print("Pip Not Installed")
    else:
        Popen([pip_version, "install", "-r", "requirements.txt"]).communicate()
        print("Installed Python Packages!")


def install_linux_dependencies():
    # Combine linux dependencies into one string
    dependencies = ["tidy"] + data.PATH_DEPENDENCIES
    check_call(
        ["sudo", "apt-get", "install", "-y", "tidy"],
        stdout=open(os.devnull, "wb"),
        stderr=STDOUT,
    )


def open_help_page():
    readme = os.path.join(os.getcwd(), "readme.html")
    webbrowser.open(readme)


def self_destruct(retain_copy=True):
    shutil.copyfile(
        os.path.join(os.getcwd(), "installer.py"),
        os.path.join(os.getcwd(), "modules\\preserved\\installer.py"),
    )
    remove(argv[0])


def _system_os_is(os):
    return platform.system().lower() == os


def install():
    if _system_os_is("windows"):
        create_desktop_shortcut("docta.py", "public/images/favicon.ico")
        install_python_modules("pip")
        open_help_page()
        self_destruct()
    elif _system_os_is("linux"):
        install_linux_dependencies()
        install_python_modules("pip3")
        open_help_page()
        self_destruct()


install()
