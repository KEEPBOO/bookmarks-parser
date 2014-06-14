#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup


def parse_bookmarks(stream):
    out_list = []
    parsed_bookmarks = BeautifulSoup(stream)

    if parsed_bookmarks.contents[0].lower() != 'netscape-bookmark-file-1':
        raise ImportError("Is not correct bookmarks file.")

    current_folder = None
    group = None

    for dt in parsed_bookmarks.findAll('dt'):
        if dt.find('h3'):
            if group:
                out_list.append(group)
            current_folder = dt.find('h3').string
            group = {
                'name': current_folder,
                'bookmarks': []
            }
        elif dt.find('a') and current_folder is not None:
            bookmark = dt.find('a')
            title = bookmark.string
            if title:
                title = title.encode('ascii', 'xmlcharrefreplace')
            group['bookmarks'].append({
                'title': title,
                'url': bookmark.get('href', ''),
                'add_date': bookmark.get('add_date', '')
            })
    if group:
        out_list.append(group)
    return out_list