from bs4 import BeautifulSoup
from werkzeug import secure_filename
import os
import shutil

PREPEND_FOLDER_NAME = "-prepend"


def get_sections(soup, separator_symbol):
    '''
    Takes in a beautiful souped html and split its according to 'chosen separator'
    Assumptions: The converted file must have a <body> tag
    '''
    body = soup.find('body')
    body_text = body.text.strip()

    if separator_symbol in body_text:  # There is a separator, go ahead

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

# Takes a list of tags and converts it to html string ( soup )


def wrap_in(string, wrap_tag):
    open = f"<{wrap_tag}>"
    close = f"</{wrap_tag}>"
    return BeautifulSoup(f"{open}{string}{close}", "html.parser")


def soupify_list(tag_list):
    # Takes a list of bs4 tags and returns a soup of them
    soup = BeautifulSoup("", "html.parser")
    body = soup.new_tag("body")
    for tag in tag_list:
        body.append(tag)
    soup.append(body)
    return soup


def sectionize(html, separators):
    if separators:
        current_sep = separators.pop(0)
        html_text = html.get_text()
        if current_sep not in html_text:
            return html
        else:
            soup = get_sections(html, current_sep)
            for level in soup.keys():
                soup[level] = sectionize(soup[level], separators.copy())
            return soup
    else:
        return html


def saveSoupToHTML(soup, file_path):
    try:
        with open(file_path, "wb") as f:
            f.write(soup.prettify("utf-8"))
            return True
    except Exception as e:
        print(f"Could not save soup. Errro: {e}")
        return False


def createFolderTree(sectionized, parent_dir):
    '''
    Takes in a sectionized document and create corresponding folders. Recursive
    '''
    if type(sectionized) == dict:
        for level in sectionized:
            print(f"level::: {level}")
            level_dir = os.path.join(parent_dir, secure_filename(level))
            print(f"Level_Dir::: {level_dir}")
            if not os._exists(level_dir):
                os.makedirs(level_dir)
            createFolderTree(sectionized[level], level_dir)
    else:
        # It must be just a string i.e. BASE CASE so create the HTML file
        html_path = os.path.join(parent_dir, "index.html")
        print(f"HTML_File::: {html_path}\n")
        saveSoupToHTML(sectionized, html_path)

        # Export the images to the files
        for img in sectionized.find_all('img'):
            image_path = img.get('src')
            if image_path:
                shutil.move(image_path, os.path.join(parent_dir, image_path))


def test(html_path):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        ssoup = sectionize(soup, ['~', '@'])
        if not os.path.exists("tester"):
            os.mkdir("tester")
        else:
            shutil.rmtree("tester")
            os.mkdir("tester")
        createFolderTree(ssoup, "tester")


test("test.html")
