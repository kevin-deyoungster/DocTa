import os
import pypandoc
import shutil
import base64
from PIL import Image
from bs4 import BeautifulSoup
from modules import mathRender

from tidylib import tidy_document

"""
    This module contains functions that are used for the basic operations such as conversion with pandoc
    and tidylib, moving files about, saving files to storage, etc. 
"""


def convert_HTML(data_string, media_destination):
    """
        Converts docx string data to html output
        : puts the images extracted in media_destination
    """
    output_html = pypandoc.convert_text(
        data_string,
        format="docx",
        to="html",
        extra_args=[r"--extract-media=" + media_destination],
    )
    # print('Converted file with Pandoc!')
    return output_html


def tidy_HTML(html_content):
    """
        Tidies html_content with TidyLib
    """
    output, errors = tidy_document(
        html_content, options={"numeric-entities": 1, "tidy-mark": 0, "wrap": 80}
    )

    # Replace smart quotes with normal quotes and em dashes to avoid char encoding errors
    output = (
        output.replace("\u2018", "&lsquo;")
        .replace("\u2019", "&rsquo;")
        .replace("\u201c", "&ldquo;")
        .replace("\u201d", "&rdquo;")
    )

    return output


def save_HTML_to_file(html_output, destination, filename):
    """
        Saves raw html output to destination + filename
    """
    output_file = os.path.join(destination, filename)
    with open(output_file, "wb") as f:
        if type(html_output) is not str:
            html_output = html_output
        else:
            html_output = html_output.encode("utf-8")
        f.write(html_output)
        return output_file


def save_BASE64_to_file(filepath, base64_string):
    """
        Saves base64 strings to file
    """
    with open(filepath, "wb") as f:
        f.write(base64.b64decode(base64_string))
    return True


def copy_images_from_folder_to_root(folder_with_images, root):
    """
        Copies images to the root directory
    """
    images_moved_count = 0
    if os.path.exists(folder_with_images):
        for media_file in os.listdir(folder_with_images):
            media_file_path = os.path.join(folder_with_images, media_file)
            dest_media_file_path = os.path.join(root, media_file)
            try:
                shutil.move(media_file_path, dest_media_file_path)
                images_moved_count += 1
            except Exception as e:
                print(e)
        os.rmdir(folder_with_images)
    print(f"\t[Image-Mover]: Moved {images_moved_count} images to job folder")


EXTENSIONS_TO_IGNORE = [".jpg", ".png", ".jpeg", ".html", ".py", ".gif"]


def normalize_media_files_in(root):
    """
        Makes sure its just pngs and jpgs in the media folder, everything else is converted
    """
    normalized_file_count = 0
    for file in os.listdir(root):
        filename = os.fsdecode(file)
        name, extension = os.path.splitext(filename)
        full_filepath = os.path.join(root, filename)
        dest_filepath = os.path.join(root, name + ".jpg")
        if extension not in EXTENSIONS_TO_IGNORE:
            normalized_file_count += 1
            Image.open(full_filepath).convert("RGB").save(dest_filepath)
            if os.path.exists(dest_filepath):
                os.remove(full_filepath)
    print(f"\t[Image-Normalizer]: Converted {normalized_file_count} images")


def delete_directory(directory):
    """
        Clears directory from existence
    """
    shutil.rmtree(directory)


def zip_up(archive_name, directory):
    """
        Compresses directory into a zip file
    """
    return shutil.make_archive(archive_name, "zip", directory)


def rename_image_files_in(root):
    img_count = 1
    index_file = os.path.join(root, "index.html")
    html_soup = BeautifulSoup(open(index_file, "rb"), "html.parser")
    images = html_soup.findAll("img")
    for image in images:
        old_image_name = image["src"]
        filename, ext = os.path.splitext(old_image_name)
        new_image_name = "image" + str(img_count).rjust(3, "0") + ext
        if old_image_name:
            old_image_path = os.path.join(root, old_image_name)
            new_image_path = os.path.join(root, new_image_name)
            if os.path.exists(old_image_path):
                os.rename(old_image_path, new_image_path)
            image["src"] = new_image_name

        img_count += 1

    f = open(index_file, "wb")
    f.write(html_soup.prettify().encode("utf-8"))
    f.close()
    print(f"\t[Image-Renamer]: Renamed {img_count} images")


def render_maths_symbols(html_soup, destination):
    """
        Renders formulas and LaTex stuff to images 
    """
    math_spans = html_soup.findAll("span", {"class": ["math inline", "math display"]})
    img_count = 1
    for math_span in math_spans:
        latex_string = math_span.text.strip().replace("\n", "")
        image_base64_string = mathRender.convert_latex_to_image(latex_string)
        if image_base64_string:
            print(f"\t[Math-Render]: Rendered {latex_string[:20]}")
            image_name = os.path.join(
                destination, "math-image-" + str(img_count) + ".png"
            )
            save_BASE64_to_file(image_name, image_base64_string)
            img_tag = html_soup.new_tag("img", src=image_name)
            math_span.replaceWith(img_tag)
            img_count += 1
    return html_soup
