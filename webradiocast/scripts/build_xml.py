# -*- coding:utf8 -*-
import sys
import os
import argparse
import ConfigParser

from webradiocast.feed import FeedManager


Parser = argparse.ArgumentParser()
Parser.add_argument('-p', dest='playlist', required=True, help='build playlist file')
Parser.add_argument('-m', dest='media', help='build target media', required=True)
Parser.add_argument('-o', dest='output', help='output to.')
Parser.add_argument(dest='config_path')


def main(argv=sys.argv):
    args = Parser.parse_args()
    if args.config_path is None:
        Parser.usage()
        exit(1)
    config = ConfigParser.SafeConfigParser()
    config.read(os.path.abspath(args.config_path))
        
    manager_ = FeedManager(os.path.abspath(args.playlist))
    if args.media is None:
        sys.stderr.write('media is reqyured.\n')
        exit(0)
    elif not manager_.has_media(args.media):
        sys.stderr.write('media "{0}" is not found.\n'.format(args.media))
        exit(1)

    builder = manager_.get_builder(args.media)
    print(builder.document.toprettyxml('  '))
    exit(0)