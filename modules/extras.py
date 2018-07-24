from bs4 import BeautifulSoup
from os import path
from .mathPolish import *


def petty_clean(html_content):
    '''
    Main entry point, runs a bunch of filters on html content and returns bs4 rendered html
    '''
    feed = BeautifulSoup(html_content, "html.parser")

    filters = [_remove_blockquotes, _convert_list_styles_to_types,
               _fix_image_styles_and_paths, _add_borders_to_table,
               _remove_header_span_ids, _remove_all_links,
               _convert_underlines]

    result = feed
    for filter in filters:
        result = filter(result)

    return result.prettify().encode('utf-8')


def _remove_blockquotes(html_soup):
    blockquotes = html_soup.findAll('blockquote')
    # print(len(blockquotes))
    for blockquote in blockquotes:
        blockquote.unwrap()
    return html_soup


list_type_dict = {
    "lower-roman": "i",
    "upper-roman": "I",
    "decimal": "1",
    "lower-alpha": "a",
    "upper-alpha": "A"
}


def _convert_list_styles_to_types(html_soup):
    ordered_lists = html_soup.findAll("ol")
    for ol in ordered_lists:
        if "style" in ol:
            style = ol["style"].split(":")[1].replace(" ", "")
            list_type = list_type_dict[style]
            del ol["style"]
            ol["type"] = list_type
    return html_soup


def _fix_image_styles_and_paths(html_soup):
    '''
    - Convert image paths from absolute to relative eg. from 'C:\.....\image1.png' -> 'image1.png'
    - Remove image height, width, alt, and style tags
    '''
    images = html_soup.findAll('img')
    for image in images:
        if image.get('height'):
            del image['height']

        if image.get('width'):
            del image['width']

        if image.get('style'):
            del image['style']

        if image.get('alt'):
            del image['alt']

        image['max-width'] = '100%'
        image['src'] = path.basename(image['src'])

    for embed in html_soup.findAll('embed'):
        embed['src'] = path.basename(embed['src']).replace(
            ".emf", ".jpg").replace(".wmf", ".jpg")
        embed.name = 'img'

    return html_soup


def _add_borders_to_table(html_soup):
    tables = html_soup.findAll("table")
    for table in tables:
        table["border"] = "1"
        trs = table.findAll('tr')
        for tr in trs:
            del tr['class']
    return html_soup


def _remove_all_links(html_soup):
    links = html_soup.findAll("a")
    for link in links:
        del link['href']
    return html_soup


def _remove_header_span_ids(html_soup):
    headings = html_soup.findAll(["h1", "h2", "h3", "span"])
    for heading in headings:
        if heading.get('id'):
            del heading['id']

        if heading.get('class'):
            if (heading.name == 'span' and heading.get('class') == "anchor") or (heading.name != 'span'):
                del heading['class']

    return html_soup


def _convert_underlines(html_soup):
    underline_spans = html_soup.findAll("span", {"class": "underline"})
    for uspan in underline_spans:
        uspan.name = 'u'
        if uspan.get('class'):
            del uspan['class']
    return html_soup


def _correct_fractions(html_soup):
    fraction_spans = html_soup.findAll(
        "span", {"class": ["math inline", "math display"]})
    for fraction_span in fraction_spans:
        stripped_fraction_line = fraction_span.text.strip()
        if "frac" in stripped_fraction_line:
            fraction_html = polish_fractions(stripped_fraction_line)
            fraction_span.replaceWith(
                BeautifulSoup(fraction_html, 'html.parser'))
    return html_soup
