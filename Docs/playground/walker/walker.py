# This module walks through every file in subfolders of a folder

# Loops through every file with extension in [targetExtensions] in folder and runs 'function on them'
import glob
import os


def walk(folder, target_extension, function):
    files = []
    for filename in glob.iglob(f"{folder}/**/*.html", recursive=True):
        file = os.path.join(folder, filename)
        function(file)
    return True


def do(param):
    print(param)


# walk("C:\\Users\\kaminoshinyu\\Dropbox\\JEC Semester 2", None, do)
