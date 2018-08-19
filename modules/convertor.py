# It seems importing just utils causes a pyton error.
from .utils import *
from .petty_clean import *

from os import path
from datetime import datetime
from werkzeug import secure_filename

LOG_TAG = "Convertor"
"""
    This module serves as the entry point for the conversion process. It utilizes all 
    the other modules and functions to successfully take files through conversion.
"""


def convert(files, job_folder, separators=None):
    """
    Main entry point
    """
    time_stamp = str(datetime.now().strftime("%m-%d-%Y.%H-%M-%S"))
    job_dir = path.join(job_folder, time_stamp)
    os.makedirs(job_dir)

    for file in files:
        file_dir = path.join(job_dir, path.splitext(secure_filename(file.filename))[0])
        f = file.read()
        _convert_file(
            {"data": f, "destination": file_dir, "filename": file.filename}, job_dir
        )
        print(f"[{LOG_TAG}]: Conversion of '{file.filename}' Complete")

    zip_of_job = zip_up(job_dir, job_dir)

    delete_directory(job_dir)

    return zip_of_job


def _convert_file(file_info, job_dir):

    print(f"\n[{LOG_TAG}]: Converting '{file_info['filename']}'")
    # Create the File's Directory [ turns out if there isn't any image in the file it won't create the folder]
    os.makedirs(file_info["destination"])

    # Create Proper Filename
    filename = os.path.splitext(file_info["filename"])[0]
    file_info["filename"] = filename

    # Convert docx file to html with Pandoc
    output_html = convert_HTML(file_info["data"], file_info["destination"])
    print(f"[{LOG_TAG}]: Converted to HTML with Pandoc")

    # Tidy up the html generated by Pandoc
    tidied_html = tidy_HTML(output_html)
    print(f"[{LOG_TAG}]: Tidied HTML with HTMLTidy")

    print(f"[{LOG_TAG}]: Petty Cleaning...")
    # Petty Clean the html: Run Custom Cleaners
    petty_cleaned_html = petty_clean(tidied_html)

    # Save the result html content to a file
    output_file = save_HTML_to_file(
        petty_cleaned_html, file_info["destination"], "index.html"
    )
    print(f"[{LOG_TAG}]: Saved to HTML")

    # Render Math Formulas if any

    # Copy the images from the media directory to the main root
    print(f"[{LOG_TAG}]: Moving Images to Main Folder")

    copy_images_from_folder_to_root(
        os.path.join(file_info["destination"], "media"), file_info["destination"]
    )

    # Copy the math images to the main root
    copy_images_from_folder_to_root("math-images", file_info["destination"])

    # Normalize those images
    print(f"[{LOG_TAG}]: Renaming Image and Normalizing them")
    normalize_media_files(file_info["destination"])

    # Rename all images again
    rename_image_files(file_info["destination"])
