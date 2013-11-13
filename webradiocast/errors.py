# -*- coding:utf8 -*-
class PlaylistNotFound(Exception):
    """プレイリストが見つからなかった時にスローされます
    """
    def __init__(self, playlist_path):
        self.playlist_path = playlist_path
    def __str__(self):
        message_ = 'Playlist file is not found. ({0})'\
            .format(self.playlist_path)
        return message_


class PlaylistException(Exception):
    pass