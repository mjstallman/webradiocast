# -*- coding:utf8 -*-
import unittest
import os
from ConfigParser import SafeConfigParser, DEFAULTSECT
from webradiocast.feed import *

from xml.dom import Node
from xml.dom.minidom import Document

from webradiocast.errors import PlaylistNotFound


MY_DIR = os.path.dirname(__file__)


class InitChannelTests(unittest.TestCase):
    def test_it(self):
        results = init_channel()
        self.assertIsInstance(results, tuple)

        self.assertIsInstance(results[0], Document)
        self.assertEqual(results[0].nodeName, '#document')
        self.assertEqual(results[0].firstChild.nodeName, 'rss')
        self.assertIsInstance(results[1], Node)
        self.assertEqual(results[1].nodeName, 'channel')
        self.assertEqual(results[1].parentNode.nodeName, 'rss')


class UpdateChannelTests(unittest.TestCase):
    def setUp(self):
        self.document, self.channel = init_channel()

    def test_simple(self):
        before_childrens = len(self.channel.childNodes)
        update_channel(self.channel, {'title': 'test'})
        after_childrens = len(self.channel.childNodes)
        self.assertGreater(after_childrens, before_childrens)
        self.assertEqual(self.channel.firstChild.nodeName, 'title')
        self.assertEqual(self.channel.firstChild.firstChild.nodeValue, 'test')

    def test_simple(self):
        update_channel(self.channel, {'title': 'test'})
        before_childrens = len(self.channel.childNodes)
        update_channel(self.channel, {'title': 'test2'}, overwrite=True)
        after_childrens = len(self.channel.childNodes)
        self.assertEqual(after_childrens, before_childrens)
        self.assertEqual(self.channel.firstChild.firstChild.nodeValue, 'test2')


class FeedBuilderTests(unittest.TestCase):
    def setUp(self):
        self.builder = FeedBuilder()
        self.playlist = ConfigParser.SafeConfigParser()
        self.playlist.read(MY_DIR+'/testdata/playlist/simple.ini')

    def test_it(self):
        self.assertTrue(hasattr(self.builder, 'document'))
        self.assertIsInstance(self.builder.document, Document)
        self.assertTrue(hasattr(self.builder, '_FeedBuilder__document'))
        self.assertTrue(hasattr(self.builder, '_FeedBuilder__channel'))
        self.assertTrue(hasattr(self.builder, 'settings'))
        builder = FeedBuilder(dict(self.playlist.items('media_name')))

    def test_update_info(self):
        self.builder.update_info({})
        #self.assertIn('<channel/>', self.builder.document.toxml())
        self.builder.update_info({'title':'test'})
        self.assertNotIn('<channel/>', self.builder.document.toxml())
        self.assertIn('<title>test</title>', self.builder.document.toxml())
        self.assertIn('<lastBuildDate>', self.builder.document.toxml())
        self.assertIn('</lastBuildDate>', self.builder.document.toxml())
        self.assertIn('<language>', self.builder.document.toxml())
        self.assertIn('</language>', self.builder.document.toxml())


    def test_find_media__direct_pathname(self):
        medias = self.builder.find_media(pathname=MY_DIR+'/testdata/media/*.mp3')
        self.assertEqual(len(medias), 4)

    def test_find_media__no_media_dir(self):
        builder = FeedBuilder(dict(self.playlist.items('media_name')))
        with self.assertRaises(PlaylistException):
            medias = builder.find_media()

    def test_find_media(self):
        builder = FeedBuilder(dict(self.playlist.items('media_name_valid')))
        try:
            medias = builder.find_media()
        except PlaylistException:
            self.fail('catch PlaylistException')
        self.assertEqual(len(medias), 4)

    def test_find_media(self):
        builder = FeedBuilder(dict(self.playlist.items('media_name_valid')))
        try:
            builder.make_feed()
        except PlaylistException:
            self.fail('catch PlaylistException')
        self.assertEqual(len(builder.document.getElementsByTagName('item')), 4)

    '''
    def test_set_config(self):
        section_ = FeedBuilder.SETTING_SECTION
        config = SafeConfigParser()
        config.add_section(section_)
        config.set(section_, 'output_dir', '15')
    '''


class FeedManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = FeedManager()

    def test_const(self):
        self.assertEqual(FeedManager.SETTING_SECTION, 'build_xml')

    def test_playlist(self):
        self.assertRaises(
            PlaylistNotFound,
            self.manager.read_playlist,
            ('not_found')
        )
        try:
            self.manager.read_playlist(MY_DIR+'/testdata/playlist/simple.ini')
        except PlaylistNotFound:
            self.fail('raised error.')
        self.assertTrue(hasattr(self.manager, '_FeedManager__playlist'))

    def test_it(self):
        self.manager.read_playlist(MY_DIR+'/testdata/playlist/simple.ini')
        self.assertTrue(self.manager.has_media('media_name'))

    def test_gnerate_builder(self):
        self.manager.read_playlist(MY_DIR+'/testdata/playlist/simple.ini')
        builder = self.manager.get_builder('media_name')
        self.assertIsInstance(builder, FeedBuilder)
        self.assertIn('<title>test_media_title</title>', builder.document.toxml())
        
    def test_generate_failed_bulder(self):
        self.assertRaises(
            PlaylistException,
            self.manager.get_builder,
            ('not_found')
        )
