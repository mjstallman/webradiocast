# -*- coding:utf8 -*-
import os
import glob
from stat import ST_SIZE
from datetime import datetime
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
    DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'
    
    def __init__(self, settings={}):
        self.__document, self.__channel = init_channel()
        self.settings = settings

    @property
    def document(self):
        return self.__document

    def update_info(self, info):
        update_channel(self.__channel, info, True)
        update_channel(self.__channel, {'language': 'ja-jp', 'lastBuildDate': datetime.now().strftime(self.DATE_FORMAT)}, True)

    def find_media(self, pathname=None):
        if pathname is not None:
            return glob.glob(pathname)
        if 'media_dir' not in self.settings:
            raise PlaylistException('setting "media_dir" is not found.')
        return glob.glob(os.path.abspath(self.settings['media_dir'])+'/*.mp3')

    def make_feed(self):
        for media in self.find_media():
            try:
                item_ = self.make_item(media)
                self.__channel.appendChild(item_)
            except ValueError as err:
                if not err.message.startswith('time data'):
                    raise err

    def make_item(self, media_path):
        item = self.__document.createElement('item')
        filename = os.path.basename(media_path)
        file_date = datetime.strptime(filename.split('.')[0], '%Y%m%d')
        elements = dict()
        elements['pubDate'] = file_date.strftime(self.DATE_FORMAT)
        elements['title'] = file_date.strftime('%Y年%m月%d日配信分')
        elements['description'] = file_date.strftime(self.settings['title']+'の%Y年%m月%d日配信分です')
        for tag, text in elements.items():
            node_ = self.__document.createElement(tag)
            node_.appendChild(self.__document.createTextNode(text))
            item.appendChild(node_)
        node_ = self.__document.createElement('enclosure')
        node_.setAttribute('url', self.settings['media_url']+'/'+filename)
        node_.setAttribute('type', 'audio/mpeg')
        node_.setAttribute('length', str(os.stat(media_path)[ST_SIZE]))
        item.appendChild(node_)
        
        return item

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
