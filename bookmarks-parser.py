#!/usr/bin/env python
# encoding: utf-8

import sys
from bs4 import BeautifulSoup

out_list = []


def parse_bookmarks(in_filename):
    global bookmarks
    try:
        parsed_bookmarks = BeautifulSoup(open(in_filename))
    except IOError:
        print 'Error.', in_filename + ' does not exist.'
        sys.exit()

    if not parsed_bookmarks.title.string == 'Bookmarks':
        print in_filename + ' does not correct bookmarks file.'
        sys.exit()

    global current_folder, group
    current_folder = None

    for dl in parsed_bookmarks.find('dl'):

        # Find folder.
        if dl.name == 'dt':
            current_folder = dl.find('h3')
            # print current_folder.string

        # Bookmarks in current folder.
        if dl.name == 'dl' and current_folder is not None:

            folder_name = current_folder.string.encode('utf-8')
            # print folder_name.encode('utf8')
            group = {'name': folder_name}
            # print group
            bookmarks_in_folder = dl.find_all('a')
            bookmarks = []
            for bookmark in bookmarks_in_folder:
                # If there is no last_modified field.
                try:
                    last_modified = bookmark['last_modified']
                except KeyError:
                    last_modified = bookmark['add_date']

                # Add bookmark to list.
                bookmarks.append({
                    'title': bookmark.string,
                    'added': bookmark['add_date'],
                    'modified': last_modified,
                    'url': bookmark['href']
                })

            # Add group to out list.
            group['bookmarks'] = bookmarks
            out_list.append(group)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Start the script like so: python bookmarks-parser.py <input_filename>.'
    else:
        input_filename = sys.argv[1]
        print 'Input filename:', input_filename
        parse_bookmarks(input_filename)
        print out_list