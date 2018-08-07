from bs4 import BeautifulSoup
from werkzeug import secure_filename


def get_sections(soup, separator):

    body = soup.find('body')

    # Gets all first-level elements in the body
    elements = body.find_all(recursive=False)
    sections = {}

    temp_track = []
    current_heading = ""
    tracking = False
    if separator in body.text.strip():
        for element in elements:
            all_element_text = element.text.strip()
            if separator in all_element_text:  # If its a marked heading

                if temp_track:  # If we're already tracking something, save section and restart
                    if current_heading == "":
                        sections["prepend"] = temp_track.copy()
                        print(
                            f"Created prepend with {len(temp_track.copy())} elements")
                        temp_track.clear()
                    else:
                        sections[current_heading] = temp_track.copy()
                        print(
                            f"Created new section {current_heading} with content")
                        temp_track.clear()

                heading = element.get_text().strip()
                current_heading = heading
                # We don't add the heading to temp track because we don't want headings in it
                print(f"Found new heading {current_heading}")
            else:  # if element is not a marked heading, just add it to the stuff

                temp_track.append(element)
                print(f"Added element {element.name} to {current_heading}")

            # If element is the last element, save section and reset
            if elements.index(element) == len(elements) - 1:
                print(f'Reached last element {current_heading}')
                sections[current_heading] = temp_track.copy()
                temp_track.clear()
        return sections
    else:
        return None


# sections = get_sections("index.html", separator)
# soups = []
# # print(sections.keys())
# for heading in sections:
#     # print("Writing to file")
#     section = sections[heading]
#     soup = BeautifulSoup("", "html.parser")
#     main = soup.new_tag("body")
#     soup.append(main)
#     # print(len(section))
#     for element in section:
#         main.append(element)

#     res = soup.prettify().encode('utf-8')
#     f = open(f"{secure_filename(heading)}.html", "wb")
#     f.write(res)
#     f.close()
# soups.append(res)


def test(html_path):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        sections = get_sections(soup, "~")
        if sections:
            print(sections.keys())
        else:
            print(f"There's no separator in it. Not doing anything")


test("index.html")
