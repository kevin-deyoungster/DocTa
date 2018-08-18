from subprocess import Popen

try:
    import winshell
except ImportError as e:
    print("Winshell package not installed. Installing winshell...")
    Popen(["pip", "install", "winshell"]).communicate()
    import winshell

import os
import shutil
import webbrowser
from win32com.client import Dispatch

from os import remove
from sys import argv


def create_desktop_shortcut(target_program, icon_path):
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


def install_python_modules():
    if not shutil.which("python"):
        print("Python Not Installed")
    elif not shutil.which("pip"):
        print("Pip Not Installed")
    else:
        Popen(["pip", "install", "-r", "requirements.txt"]).communicate()
        print("Installed Python Packages!")


def open_help_page():
    readme = os.path.join(os.getcwd(), "readme.html")
    webbrowser.open(readme)


def self_destruct(retain_copy=True):
    shutil.copyfile(
        os.path.join(os.getcwd(), "install.py"),
        os.path.join(os.getcwd(), "modules\\preserved\\install.py"),
    )
    remove(argv[0])


create_desktop_shortcut("docta.py", "static/images/favicon.ico")
install_python_modules()
open_help_page()
self_destruct()
