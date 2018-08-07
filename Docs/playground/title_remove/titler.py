from bs4 import BeautifulSoup


def remove_title(html_file_path):
    try:
        with open(html_file_path, encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            body = soup.find('body')
            if body:
                # print("There is a body here, remove first element in the body tag")
                heading = body.find()
                body.find().decompose()
                result = soup.prettify().encode('utf-8')
                newfile = open(f"{html_file_path}", 'wb')
                newfile.write(result)
                newfile.close()
                # print(body.find())
            else:
                # print("There isn't a body. Removing first element")
                # print(soup.find())
                soup.find().decompose()
                result = soup.prettify().encode('utf-8')
                newfile = open(f"{html_file_path}", 'wb')
                newfile.write(result)
                newfile.close()
        pass
    except Exception as e:
        print(f"\nCould not read {html_file_path}")
        # print(e)


# remove_title(
#     "C:\\Users\\kaminoshinyu\\Desktop\\DocTa\\docs\\playground\\title_remove\\no body.html")
# remove_title(
    # "C:\\Users\\kaminoshinyu\\Desktop\\DocTa\\docs\\playground\\title_remove\\with body.html")
