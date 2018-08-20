from bs4 import BeautifulSoup
from os import path
from .utils import *

LOG_TAG = "Petty-Clean"


def petty_clean(html_content):
    """
    Main entry point, runs a bunch of filters on html content and returns bs4 soup
    """
    feed = BeautifulSoup(html_content, "html.parser")

    filters = [
        _remove_blockquotes,
        _convert_list_styles_to_types,
        _fix_image_styles_and_paths,
        _add_borders_to_table,
        _remove_header_span_ids,
        _remove_all_links,
        _convert_underlines,
    ]

    result = feed
    for filter in filters:
        result = filter(result)

    return result


def _remove_blockquotes(html_soup):
    """
    Some lists have blockquotes (creating extra space btn number and text)
    """
    blockquotes = html_soup.findAll("blockquote")
    for blockquote in blockquotes:
        blockquote.unwrap()
    print(f"\t[{LOG_TAG}]: Removed {len(blockquotes)} Blockquotes")
    return html_soup


list_type_of_style = {
    "lower-roman": "i",
    "upper-roman": "I",
    "decimal": "1",
    "lower-alpha": "a",
    "upper-alpha": "A",
}


def _convert_list_styles_to_types(html_soup):
    """
    Because we don't want classes...
    Convert list styles to types eg. from [ <ol class='lower-roman'> ] -> [ <ol style='i'> ]
    """
    ordered_lists = html_soup.findAll("ol")
    lists_changed = 0
    for ordered_list in ordered_lists:
        if "style" in ordered_list:
            style = ordered_list["style"].split(":")[1].replace(" ", "")
            list_type = list_type_of_style[style]
            del ordered_list["style"]
            ordered_list["type"] = list_type
            lists_changed += 1
    print(f"\t[{LOG_TAG}]: Converted {lists_changed} Lists from class to style")
    return html_soup


def _fix_image_styles_and_paths(html_soup):
    """
    - Convert image paths from absolute to relative eg. from [ 'C:\.....\image1.png' ] -> [ 'image1.png' ]
    - Remove image height, width, alt, and style tags
    """
    images = html_soup.findAll("img")
    for image in images:
        _del_attribute(image, "height")
        _del_attribute(image, "width")
        _del_attribute(image, "style")
        _del_attribute(image, "alt")
        # Can't use image.pop() because image is bs4 Tag, not normal dictionary
        image["max-width"] = "100%"
        image["src"] = path.basename(image["src"])
    print(f"\t[{LOG_TAG}]: Fixed {len(images)} Images")
    for embed in html_soup.findAll("embed"):
        embed["src"] = (
            path.basename(embed["src"]).replace(".emf", ".jpg").replace(".wmf", ".jpg")
        )
        embed.name = "img"

    return html_soup


def _del_attribute(dict, attribute):
    """
    Deletes [attribute] from dictionary if it exists
    """
    if dict.get(attribute):
        del dict[attribute]


def _add_borders_to_table(html_soup):
    tables = html_soup.findAll("table")
    for table in tables:
        table["border"] = "1"
        trs = table.findAll("tr")
        for tr in trs:
            del tr["class"]
    print(f"\t[{LOG_TAG}]: Added Borders to {len(tables)} Tables")

    return html_soup


def _remove_all_links(html_soup):
    links = html_soup.findAll("a", href=True)
    for link in links:
        del link["href"]
    print(f"\t[{LOG_TAG}]: Removed {len(links)} Hyperlinks")

    return html_soup


def _remove_header_span_ids(html_soup):
    headings = html_soup.findAll(["h1", "h2", "h3", "span"])
    removed = 0
    for heading in headings:
        if heading.get("id"):
            del heading["id"]
            removed += 1
        if heading.get("class"):
            if (heading.name == "span" and heading.get("class") == "anchor") or (
                heading.name != "span"
            ):  # Get all span class='anchors', leave all other spans ( some may be underline / math images)
                del heading["class"]
                removed += 1
    print(f"\t[{LOG_TAG}]: Removed IDs and Classes of {removed} Text Elements")

    return html_soup


def _convert_underlines(html_soup):
    underline_spans = html_soup.findAll("span", {"class": "underline"})
    for uspan in underline_spans:
        uspan.name = "u"
        if uspan.get("class"):
            del uspan["class"]
    print(f"\t[{LOG_TAG}]: Corrected {len(underline_spans)} Underlines")
    return html_soup
