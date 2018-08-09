from bs4 import BeautifulSoup
from werkzeug import secure_filename
import os
import shutil


def wrap_in(string, wrap_tag):
    '''
    Wraps [string] in html tag [wrap_tag]
    '''
    open = f"<{wrap_tag}>"
    close = f"</{wrap_tag}>"
    return BeautifulSoup(f"{open}{string}{close}", "html.parser")


TEST_FOLDER = "tester"
PREPEND_FOLDER_NAME = "-prepend"


def get_sections(soup, separator_symbol):
    '''
    Takes in a beautiful souped html and splits its according to 'chosen separator'
    Assumptions: The converted file must have a <body> tag
    '''
    body = soup.find('body')
    body_text = body.text.strip()

    if separator_symbol in body_text:  # There is a separator, go ahea
        sections = {}
        temp_html = ""
        current_heading = ""
        tags_in_body = body.find_all(recursive=False)  # first-level tags

        for tag in tags_in_body:
            tag_text = tag.text.strip()

            if separator_symbol in tag_text:  # If its a marked heading
                if temp_html != "":  # If we're already tracking something, save section and restart
                    if current_heading == "":  # No heading has been seen yet, meaning its a prepend
                        heading = PREPEND_FOLDER_NAME
                    else:
                        heading = current_heading
                    sections[heading] = wrap_in(temp_html, "body")
                    temp_html = ""
                # We don't add the heading to temp track
                current_heading = tag_text.replace(separator_symbol, "")

            else:  # if element is not a marked heading, just add it to the stuff
                temp_html += str(tag)

            # If element is the last element, save section and reset
            if tags_in_body.index(tag) == len(tags_in_body) - 1:
                sections[current_heading] = wrap_in(temp_html, "body")
                temp_html = ""
        return sections
    else:  # there is no separator, don't bother yourself
        return soup


def split(html, separators):
    '''
    The main splitting code. Recursive algorithm
    '''
    if separators:
        first_separator = separators.pop(0)
        html_text = html.get_text()
        if first_separator not in html_text:
            return html
        else:
            soup = get_sections(html, first_separator)
            for section in soup.keys():
                soup[section] = split(soup[section], separators.copy())
            return soup
    else:
        return html


def saveSoupToHTML(soup, file_path):
    '''
    Saves beautiful soup object to html file
    '''
    try:
        with open(file_path, "wb") as f:
            f.write(soup.prettify("utf-8"))
            return True
    except Exception as e:
        print(f"Could not save soup. Error: {e}")
        return False


def createFolderTree(sections, parent_dir):
    '''
    Takes in sections and creates corresponding folders. Recursive
    '''
    if type(sections) == dict:  # Section has subsections
        for heading in sections:
            heading_dir = os.path.join(parent_dir, secure_filename(heading))
            os.makedirs(heading_dir)
            createFolderTree(sections[heading], heading_dir)
    elif type(sections) == BeautifulSoup:  # Section is actually html code. Base case
        html_path = os.path.join(parent_dir, "index.html")
        # print(f"::HTML_File::: {html_path}\n")
        saveSoupToHTML(sections, html_path)

        # Export the images in this file to its directory
        for img in sections.find_all('img'):
            image_path = img.get('src')
            if image_path:
                shutil.move(image_path, os.path.join(parent_dir, image_path))
    else:
        print(f"<===> Eih, What is a {type(sections)}")


def test(html_path):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        sections = split(soup, ['~', '@'])

        if not os.path.exists(TEST_FOLDER):
            os.mkdir(TEST_FOLDER)
        else:
            shutil.rmtree(TEST_FOLDER)
            os.mkdir(TEST_FOLDER)

        createFolderTree(sections, TEST_FOLDER)


test("test.html")
