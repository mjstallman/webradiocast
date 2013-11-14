# -*- coding:utf8 -*-
import os
import glob
import ConfigParser
from xml.dom.minidom import Node, getDOMImplementation

from .errors import PlaylistNotFound, PlaylistException

def init_channel():
    """Podcast用フィードの設定初期DOMを生成する
    """
    document = getDOMImplementation().createDocument(None, 'rss', None)
    channel = document.createElement('channel')
    document.documentElement.appendChild(channel)
    return (document, channel)


def update_channel(channel_node, children_dict, overwrite=False):
    """channel直下のnodeを追加登録する
    """
    document_ = channel_node.parentNode.parentNode
    for tag, text in children_dict.items():
        node_ = document_.createElement(tag)
        node_.appendChild(document_.createTextNode(text))
        old_tags = channel_node.getElementsByTagName(tag)
        if len(old_tags) >= 1 and overwrite:
            channel_node.replaceChild(node_, old_tags[0])
        else:
            channel_node.appendChild(node_)

    return channel_node


class FeedBuilder(object):
    """フィード組み立て用クラス
    """
    def __init__(self, settings={}):
        self.__document, self.__channel = init_channel()
        self.settings = settings

    @property
    def document(self):
        return self.__document

    def update_info(self, info):
        update_channel(self.__channel, info, True)

    def find_media(self, pathname=None):
        if pathname is not None:
            return glob.glob(pathname)
        if 'media_dir' not in self.settings:
            raise PlaylistException('setting "media_dir" is not found.')
        return glob.glob(os.path.abspath(self.settings['media_dir'])+'/*')

    def make_feed(self):
        for media in self.find_media():
            item_ = self.__document.createElement('item')
            self.__channel.appendChild(item_)
            

class FeedManager(object):
    """
    """
    SETTING_SECTION = 'build_xml'

    def __init__(self, playlist_path=None):
        if playlist_path is not None:
            self.read_playlist(playlist_path)
        else:
            self.__playlist = ConfigParser.SafeConfigParser()

    def read_playlist(self, playlist_path):
        if not os.path.exists(playlist_path):
            raise PlaylistNotFound(playlist_path)
        self.__playlist = ConfigParser.SafeConfigParser()
        self.__playlist.read(playlist_path)

    def has_media(self, media_name):
        return (media_name in self.__playlist.sections())

    def get_builder(self, media_name):
        if not self.has_media(media_name):
            raise PlaylistException()
        builder = FeedBuilder(dict(self.__playlist.items(media_name)))
        builder.update_info(builder.settings)
        return builder
