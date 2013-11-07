# -*- coding:utf8 -*-
from xml.dom.minidom import Node, getDOMImplementation


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
        if overwrite:
            old_tag = channel_node.getElementsByTagName(tag)[0]
            channel_node.replaceChild(node_, old_tag)
        else:
            channel_node.appendChild(node_)

    return channel_node
