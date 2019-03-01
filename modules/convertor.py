from uuid import uuid4
from pathlib import Path
from werkzeug.utils import secure_filename

from modules import utils as UTILITIES

# from modules import splita as SPLITTER
from modules import splitter as SPLITTER
from modules import petty_clean as PETTY_CLEANER


LOG_TAG = "Convertor"
SPLIT_MARKS = ["~", "@", "$"]
"""
    This module serves as the entry point for the conversion process. It utilizes all 
    the other modules and functions to successfully take files through conversion.
"""


def convert(documents, job_folder):
    jobs_dir = Path(job_folder) / str(uuid4())
    jobs_dir.mkdir(parents=True)

    for doc in documents:
        extension = Path(doc.filename).suffix
        doc_filename = secure_filename(
            Path(doc.filename).stem
        )  # Remove invalid filename chars.
        doc_dir = jobs_dir / doc_filename

        info = {"content": doc.read(), "destination": doc_dir, "filename": doc_filename}
        if extension == ".pptx":
            __convert_slides(info)
        elif extension == ".docx":
            __convert_doc(info)
        else:
            print(f"[{LOG_TAG}]: Unsupported Extension")
        print(f"[{LOG_TAG}]: Conversion of '{doc_filename}' Complete")

    zip_of_jobs = UTILITIES.zip_up(jobs_dir, jobs_dir)

    UTILITIES.delete_directory(jobs_dir)

    return zip_of_jobs


def __convert_doc(doc_info):
    DESTINATION = doc_info["destination"]
    FILE_CONTENT = doc_info["content"]
    FILENAME = doc_info["filename"]

    print(f"\n[{LOG_TAG}]: Converting '{FILENAME}'")

    # Create the File's Directory [ because if there isn't any image in the file it won't create the folder]
    DESTINATION.mkdir(parents=True, exist_ok=True)

    # Convert docx file to html with Pandoc
    output_html = UTILITIES.convert_HTML(FILE_CONTENT, str(DESTINATION))
    print(f"[{LOG_TAG}]: Converted to HTML with Pandoc")

    # Tidy up the html generated by Pandoc
    tidied_html = UTILITIES.tidy_HTML(output_html)
    print(f"[{LOG_TAG}]: Tidied HTML with HTMLTidy")

    # Render Math Formulas if needed
    print(f"[{LOG_TAG}]: Checking for Math Formulas...")
    math_rendered_soup = UTILITIES.render_maths(tidied_html, DESTINATION)

    # Petty Clean the html: Run Custom Cleaners
    print(f"[{LOG_TAG}]: Petty Cleaning...")
    petty_cleaned_soup = PETTY_CLEANER.petty_clean(math_rendered_soup)

    # Save the result html content to a file
    converted_doc = petty_cleaned_soup.prettify().encode("utf-8")
    UTILITIES.save_HTML(converted_doc, DESTINATION, "index.html")
    print(f"[{LOG_TAG}]: Saved HTML File")

    # Copy the images from the media directory to the main root
    print(f"[{LOG_TAG}]: Moving Images to Root Folder...")
    media_folder = DESTINATION / "media"
    UTILITIES.move_files(media_folder, DESTINATION)

    # Convert all non-supported images to supported format
    print(f"[{LOG_TAG}]: Converting Invalid Images...")
    UTILITIES.convert_invalid_images_in(DESTINATION)

    # Rename images with proper count
    print(f"[{LOG_TAG}]: Renaming All Images...")
    UTILITIES.rename_image_files_in(DESTINATION)

    # Split the file
    print(f"[{LOG_TAG}]: Checking for Split-Marks...")
    index_html = DESTINATION / "index.html"
    SPLITTER.split_into_sections(index_html, SPLIT_MARKS.copy(), DESTINATION)


def __convert_slides(slides_info):
    TAG = "Slide-Worker"
    DESTINATION = slides_info["destination"]
    DESTINATION.mkdir(parents=True, exist_ok=True)

    FILE_CONTENT = slides_info["content"]
    FILE_NAME = secure_filename(slides_info["filename"] + ".pptx")
    OUTPUT_PATH = DESTINATION / FILE_NAME
    with open(OUTPUT_PATH, "wb") as f:
        f.write(FILE_CONTENT)

    if Path(OUTPUT_PATH).exists():
        has_converted = SLIDE_UTILITIES.export_slides(OUTPUT_PATH, DESTINATION)
        if has_converted:
            print(f"[{TAG}]: Converted Slides")
            slide_soup = SLIDE_UTILITIES.knit_images_to_soup(DESTINATION)
            slide_HTML = slide_soup.prettify("utf-8")
            UTILITIES.save_HTML(slide_HTML, DESTINATION, "index.html")
        else:
            print(f"[{TAG}]: Failed to convert slides")
    else:
        print(f"[Slide-Worker]: Could not save {slides_info['filename']} to file")

