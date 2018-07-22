import os
import pypandoc
import shutil

from tidylib import tidy_document


def convert_HTML(data_string, media_destination):
    '''
        Converts docx data to html output
    '''
    output_html = pypandoc.convert_text(
        data_string, format='docx', to='html', extra_args=[r'--extract-media=' + media_destination])
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

    # Replace smart quotes with normal quotes to avoid char encoding errors
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
            html_output = str(html_output.encode('utf-8'))
        else:
            html_output = html_output.encode('utf-8')
        f.write(html_output)
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


def delete_directory(directory):
    shutil.rmtree(directory)


def zip_up(archive_name, directory):
    return shutil.make_archive(archive_name, 'zip', directory)
