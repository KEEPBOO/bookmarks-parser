#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup


out_list = []


def parse_bookmarks(stream):
    parsed_bookmarks = BeautifulSoup(stream)

    if parsed_bookmarks.contents[0].lower() != 'netscape-bookmark-file-1':
        raise ImportError("Does not correct bookmarks file.")

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

        if dt.find('a') and current_folder is not None:
            bookmark = dt.find('a')
            group['bookmarks'].append({
                'title': bookmark.string,
                'url': bookmark.get('href', ''),
                'add_date': bookmark.get('add_date', '')
            })
    if group:
        out_list.append(group)
    return out_list