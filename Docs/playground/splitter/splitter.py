from bs4 import BeautifulSoup
from werkzeug import secure_filename

separator = "~"


def getSections(html_path, separator):
    with open(html_path, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
        body = soup.find('body')
        allElements = body.find_all(recursive=False)
        sections = {}
        track = False
        temp_track = []
        current_heading = ""
        tracking = False
        for element in allElements:
            if separator in element.text.strip():
                if temp_track:
                    sections[current_heading] = temp_track.copy()
                    print(
                        f"Created new section {current_heading} with content")
                    temp_track.clear()

                heading = element.get_text().strip()
                current_heading = heading

                print(f"Found new heading {current_heading}")

                # # print("This is a new heading, restarting")
                # sections[current_heading] = temp_track.copy()
                # print(
                #     f"Created new section {current_heading} with content")
                # temp_track.clear()
            else:
                temp_track.append(element)
                print(f"Added element {element.name} to {current_heading}")

                # If you reached the last element
                if allElements.index(element) == len(allElements) - 1:
                    print(f'Reached last element {heading}')
                    sections[current_heading] = temp_track.copy()
                    temp_track.clear()
    print(sections.keys())
    return sections


sections = getSections("index.html", separator)
soups = []
# print(sections.keys())
for heading in sections:
    # print("Writing to file")
    section = sections[heading]
    soup = BeautifulSoup("", "html.parser")
    main = soup.new_tag("body")
    soup.append(main)
    # print(len(section))
    for element in section:
        main.append(element)

    res = soup.prettify().encode('utf-8')
    f = open(f"{secure_filename(heading)}.html", "wb")
    f.write(res)
    f.close()
# soups.append(res)
