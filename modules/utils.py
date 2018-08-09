import os
import pypandoc
import shutil
import base64
from PIL import Image
from bs4 import BeautifulSoup
from tidylib import tidy_document

'''
    This module contains functions that are used for the basic operations such as conversion with pandoc
    and tidylib, moving files about, saving files to storage, etc. 
'''


def convert_HTML(data_string, media_destination):
    '''
        Converts docx string data to html output
        : puts the images extracted in media_destination
    '''
    output_html = pypandoc.convert_text(
        data_string, format='docx', to='html', extra_args=[r'--extract-media=' + media_destination])
    # print('Converted file with Pandoc!')
    return output_html


def tidy_HTML(html_content):
    '''
        Tidies html_content with TidyLib
    '''
    output, errors = tidy_document(html_content,  options={
        'numeric-entities': 1,
        'tidy-mark': 0,
        'wrap': 80,
    })

    # Replace smart quotes with normal quotes and em dashes to avoid char encoding errors
    output = output.replace(u"\u2018", '&lsquo;').replace(
        u"\u2019", '&rsquo;').replace(u"\u201c", "&ldquo;").replace(
        u"\u201d", "&rdquo;")

    return output


def save_HTML_to_file(html_output, destination, filename):
    '''
        Saves raw html output to destination + filename
    '''
    output_file = os.path.join(destination, filename)
    with open(output_file, 'wb') as f:
        if type(html_output) is not str:
            html_output = html_output
        else:
            html_output = html_output.encode('utf-8')
        f.write(html_output)
        return output_file


def save_BASE64_to_file(filepath, base64_string):
    '''
        Saves base64 strings to file
    '''
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(base64_string))
    return True


def copy_media_to_root(root):
    '''
        Copies media files extracted by pandoc, to the root directory
    '''
    media_folder = os.path.join(root, 'media')
    if os.path.exists(media_folder):
        for media_file in os.listdir(media_folder):
            media_file_path = os.path.join(media_folder, media_file)
            shutil.move(media_file_path, root)
        os.rmdir(media_folder)


def copy_math_images_to_root(math_images_folder, root):
    '''
        Copies math images to the root directory
    '''
    if os.path.exists(math_images_folder):
        for media_file in os.listdir(math_images_folder):
            media_file_path = os.path.join(math_images_folder, media_file)
            shutil.move(media_file_path, root)
        os.rmdir(math_images_folder)


ignore_extensions = ['.jpg', '.png', '.jpeg', '.html', '.py']


def normalize_media_files(root):
    '''
        Makes sure its just pngs and jpgs in the media folder, everything else is converted
    '''
    for file in os.listdir(root):
        filename = os.fsdecode(file)
        name, extension = os.path.splitext(filename)
        full_filepath = os.path.join(root, filename)
        dest_filepath = os.path.join(root, name + '.jpg')
        if extension not in ignore_extensions:
            Image.open(full_filepath).save(dest_filepath)
            # CLean up afterwards
            if os.path.exists(dest_filepath):
                os.remove(full_filepath)


def delete_directory(directory):
    '''
        Clears directory from existence
    '''
    shutil.rmtree(directory)


def zip_up(archive_name, directory):
    '''
        Compresses directory into a zip file
    '''
    return shutil.make_archive(archive_name, 'zip', directory)


exceptions = ['.html']


def rename_image_files(root):
    img_count = 1
    # Get the index html file
    index_file = os.path.join(root, 'index.html')
    html_soup = BeautifulSoup(open(index_file, 'rb'), 'html.parser')
    images = html_soup.findAll('img')
    for image in images:
        old_image_name = image['src']
        filename, ext = os.path.splitext(old_image_name)
        new_image_name = 'image' + str(img_count).rjust(3, '0') + ext
        if old_image_name:
            old_image_path = os.path.join(root, old_image_name)
            new_image_path = os.path.join(root, new_image_name)

            # Check if the image file actually exists,
            if os.path.exists(old_image_path):
                os.rename(old_image_path, new_image_path)
                image['src'] = new_image_name

        img_count += 1
    f = open(index_file, 'wb')
    f.write(html_soup.prettify().encode('utf-8'))
    f.close()
