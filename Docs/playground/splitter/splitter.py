from bs4 import BeautifulSoup
from werkzeug import secure_filename
import os
import shutil


def get_sections(soup, chosen_separator):
    body = soup.find('body')
    # Gets all first-level elements in the body
    elements = body.find_all(recursive=False)
    sections = {}

    temp_track = []
    current_heading = ""
    tracking = False
    if chosen_separator in body.text.strip():
        for element in elements:
            all_element_text = element.text.strip()
            if chosen_separator in all_element_text:  # If its a marked heading
                if temp_track:  # If we're already tracking something, save section and restart
                    if current_heading == "":
                        sections["prepend"] = soupify_list(temp_track.copy())
                        # print(
                        # f"Created prepend with {len(temp_track.copy())} elements")
                        temp_track.clear()
                    else:
                        sections[current_heading.replace(chosen_separator, "")] = soupify_list(
                            temp_track.copy())
                        # print(
                        #     f"section {current_heading} with {len(temp_track.copy())} elements")
                        temp_track.clear()

                heading = element.get_text().strip()
                current_heading = heading
                # We don't add the heading to temp track because we don't want headings in it
                # print(f"Found new heading {current_heading}")
            else:  # if element is not a marked heading, just add it to the stuff

                temp_track.append(element)
                # print(f"Added element {element.name} to {current_heading}")

            # If element is the last element, save section and reset
            if elements.index(element) == len(elements) - 1:
                # print(f'Reached last element added to {current_heading}')
                sections[current_heading.replace(
                    chosen_separator, "")] = soupify_list(temp_track.copy())
                # print(
                # f"Created last section {current_heading} with {len(temp_track.copy())} elements\n")
                temp_track.clear()
        return sections
    else:
        return soup

# Takes a list of tags and converts it to html string ( soup )


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
        print(e)
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
            os.mkdir(level_dir)
            createFolderTree(sectionized[level], level_dir)
    else:
        # It must be just a string i.e. BASE CASE so create the HTML file
        html_path = os.path.join(parent_dir, "index.html")
        print(f"HTML_File::: {html_path}\n")
        saveSoupToHTML(sectionized, html_path)

        # Export the images to the files
        for img in sectionized.find_all('img'):
            image_path = img.get('src')
            shutil.move(image_path, os.path.join(parent_dir, image_path))


def test(html_path):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        ssoup = sectionize(soup, ['~', '@'])
        createFolderTree(ssoup, "tester")


test("index.html")
