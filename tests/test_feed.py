import unittest

from webradiocast.feed import *

from xml.dom import Node
from xml.dom.minidom import Document


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
