#!/usr/bin/env python
# encoding: utf-8

import sys
from keepoo_bookmarksparser.parser import parse_bookmarks


""" Parses a bookmarks.html file and print json result """
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'file name parameter is required'
        exit(1)
    else:
        input_filename = sys.argv[1]
        print 'Input filename:', input_filename
        try:
            print parse_bookmarks(open(input_filename))
        except IOError:
            print 'Error.', input_filename + ' does not exist.'
            exit(1)
        except ImportError, e:
            print 'Error.', e
            exit(1)
        exit(0)