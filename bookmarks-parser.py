__author__ = 'Prin53'

import sys

# Constants.
END_OF_FOLDER = "</DL><p>"
BEGIN_OF_FOLDER = "<DT><H3 ADD_DATE="
LINK = "<DT><A"
HEADER = '<!DOCTYPE NETSCAPE-Bookmark-file-1>'
ADD_DATE = "ADD_DATE="
LAST_MODIFIED = "LAST_MODIFIED="
HREF = "HREF="
ICON = "ICON="

NAME = "name"
BOOKMARKS = "bookmarks"
TITLE = "title"
ADDED = "added"
MODIFIED = "modified"
URL = "url"

out_list = []
bookmarks = {}


def print_output(out_filename):
    out_file = open(out_filename, 'w+')
    if len(out_list) > 0:
        out_file.write("[\n")
        for group in out_list:
            out_file.write("     {\n")
            out_file.write("         'name': '" + group[NAME] + "',\n")
            out_file.write("         'bookmarks': [\n")
            for bookmark in group[BOOKMARKS]:
                out_file.write("             {\n")
                out_file.write("                 'title': " + bookmark[TITLE] + ",\n")
                out_file.write("                 'added': " + bookmark[ADDED] + ",\n")
                out_file.write("                 'modified': " + bookmark[MODIFIED] + ",\n")
                out_file.write("                 'url': " + bookmark[URL] + ",\n")
                out_file.write("             }\n")
            out_file.write("         ]\n")
            out_file.write("     }\n")
        out_file.write("]\n")
    out_file.close()


def create_output():
    #[
    #     {
    #         "name": "Group1",
    #         "bookmarks": [
    #             {
    #                 "title": "Some bookmark title",
    #                 "added": "timestamp",
    #                 "modified": "timestamp",
    #                 "url": "http://"
    #             }
    #         ]
    #     }
    # ]
    for folder in bookmarks:
        group = {NAME: folder,
                 BOOKMARKS: bookmarks[folder]}
        out_list.append(group)


def parse_bookmarks(in_filename):
    global bookmarks
    #   Input file.
    try:
        in_file = open(in_filename, 'r+')
    except IOError:
        print(in_filename + ' does not exist.')
        sys.exit()

    #   Read in the whole input file.
    file_lines_list = in_file.readlines()
    in_file.close()

    current_folder = ""

    if file_lines_list[0].strip() != HEADER:
        print('Improperly formatted Bookmark File.')
        sys.exit()

    for ln in file_lines_list:
        #   Remove all leading whitespace.
        line = ln.lstrip()

        if line.startswith(BEGIN_OF_FOLDER):
            #   This line tells us about a folder.
            #   Find the next '>' after the prefix.
            left_position = line.find('>', len(BEGIN_OF_FOLDER))
            if left_position > 0:
                #   Find the next '<' after the '>'.
                right_position = line.find('<', left_position)
                #   Extract the folder name.
                current_folder = line[left_position + 1:right_position]

        elif line.startswith(END_OF_FOLDER):
            current_folder = ""

        elif line.startswith(LINK):
            #	We've found a link, let's grab the information from it.
            link_begin = line.find(HREF, len(LINK))
            link_end = line.find('"', link_begin + 6)
            #	Let's get the link.
            the_link = line[link_begin + 6:link_end]
            # print(the_link)

            #	Make sure it's a real link and not one for the browser, break if it's not.
            if the_link[:4] == 'http':
                #	Let's get the title.
                link_title = line[line.find('>', link_end) + 1:line.find('<', link_end)]
                # print(link_title)

                #	Let's get the add date.
                link_date_add_begin = line.find(ADD_DATE, len(LINK))
                link_date_add_end = line.find('"', link_date_add_begin + 10)
                link_add_date = line[link_date_add_begin + 10:link_date_add_end]
                # print(link_add_date)

                #	Let's get the last modified date. Equals add date.
                link_date_modified_begin = line.find(LAST_MODIFIED, len(LINK))
                if link_date_modified_begin == -1:
                    link_modified_date = link_add_date
                else:
                    link_date_modified_end = line.find('"', link_date_modified_begin + 15)
                    link_modified_date = line[link_date_modified_begin + 15:link_date_modified_end]

                #   Create dict of bookmark.
                bookmark = {URL: the_link,
                            MODIFIED: link_modified_date,
                            ADDED: link_add_date,
                            TITLE: link_title}

                # Add bookmark to bookmarks.
                if len(bookmarks) > 0 and current_folder in bookmarks:
                    bookmarks[current_folder].append(bookmark)
                else:
                    bookmarks[current_folder] = [bookmark]

    create_output()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Start the script like so: python bookmarks-parser.py <input_filename> <output_filename>.")
    else:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
        print("Input filename: " + input_filename + "\nOutput filename: " + output_filename)
        parse_bookmarks(input_filename)
        print("Parsing...")
        print_output(output_filename)
        print("Done.")
