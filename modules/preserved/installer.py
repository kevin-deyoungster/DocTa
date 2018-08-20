import os
import shutil
from subprocess import Popen


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


def install_python_modules():
    if not shutil.which("python"):
        print("Python Not Installed")
    elif not shutil.which("pip"):
        print("Pip Not Installed")
    else:
        Popen(["pip", "install", "-r", "requirements.txt"]).communicate()
        print("Installed Python Packages!")


def install():
    create_desktop_shortcut("docta.py", "public/images/favicon.ico")
    install_python_modules()


install()
