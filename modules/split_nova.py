import re
import pprint
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import os
import shutil

LOG_TAG = "Splitter"


def get_parent_before_body(node):
    """
    Headings are usually like: heading_text < strong < p < body. Calling text.parent.parent won't work in exceptions like:heading_text < p < body.
    This function handles getting the right parent despite depth
    """
    parent_after_body = None
    for parent in node.parents:
        if parent.name == "body":
            break
        else:
            parent_after_body = parent
    return parent_after_body


def get_html_wrapped_soup(html_string):
    return BeautifulSoup(f"<html><body>{html_string}</body></html>", "html.parser")


def _saveSoupToHTML(soup, file_path):
    """
    Saves beautiful soup object to html file
    """
    try:
        with open(file_path, "wb") as f:
            f.write(soup.prettify("utf-8"))
            return True
    except Exception as e:
        print(f"Could not save soup. Error: {e}")
        return False


def split_up(soup, separator):
    if len(separator) > 0:
        body = soup.find("body")
        all_tags = body.find_all(recursive=False)

        headings = [
            get_parent_before_body(heading)
            for heading in body.find_all(text=re.compile(separator[0]))
        ]
        if headings:  # If some headings were found with the separator
            # Get Indices of Headings
            sections = []  # List of headings and their indices
            for heading in headings:
                heading_text = heading.get_text().strip()
                heading_index = all_tags.index(heading)
                sections.append((heading_text, heading_index))

            # Split all_tags up into sections, starting from bottom
            sections_dict = {}
            all_tags_string = [str(tag) for tag in all_tags]
            for heading, index in reversed(sections):
                section_string = "".join(all_tags_string[index + 1 :])
                sections_dict[heading] = split_up(
                    get_html_wrapped_soup(section_string), separator[1:]
                )
                del all_tags[index:]
                del all_tags_string[index:]

            # At the end you'll be left with any left overs
            sections_dict["prepend"] = split_up(
                get_html_wrapped_soup("".join(all_tags_string)), separator[1:]
            )
            return sections_dict

        else:  # If no headings, it must just be html
            return soup
    else:
        return soup


def _createFolderTree(pre, the_parent, sections, parent_dir):
    """
    Takes in sections and creates corresponding folders. Recursive
    """
    if type(sections) == dict:  # Section has subsections
        for heading in sections:
            print(pre + "\t", heading, type(sections))
            heading_dir = os.path.join(parent_dir, secure_filename(heading))
            os.makedirs(heading_dir)
            _createFolderTree(pre + "\t", the_parent, sections[heading], heading_dir)
    elif type(sections) == BeautifulSoup:  # Section is actually html code. Base case
        print(pre + "\t", "Created HTML")
        html_path = os.path.join(parent_dir, "index.html")
        _saveSoupToHTML(sections, html_path)

        # Export the images in this file to its directory
        for img in sections.find_all("img"):
            image_path = os.path.join(the_parent, img.get("src"))
            target_image_path = os.path.join(parent_dir, img.get("src"))
            if os.path.exists(image_path):
                shutil.move(image_path, target_image_path)
    else:
        print(f"<===> Eih, What is a {type(sections)}")


def split_into_sections(html_path, separators, parent_folder):
    with open(html_path, encoding="utf-8") as f:
        content = f.read()
        if separators[0] in content:
            soup = BeautifulSoup(content, "html.parser")
            sections = split_up(soup, separators)
            import json

            print(sections.keys())
            print(type(sections))
            print(type(sections["~SCREEN 5"]))

            _createFolderTree("", parent_folder, sections, parent_folder)
        else:
            print(f"\t[{LOG_TAG}]: No Split Marks Detected")

