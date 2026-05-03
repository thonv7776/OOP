"""
Views Package
Contains UI components for the Jukebox application.
"""

from views.main_view import MainView
from views.track_view import TrackView
from views.playlist_view import PlaylistView
from views.favorite_view import FavoriteView
from views.play_view import PlayView

__all__ = ['MainView', 'TrackView', 'PlaylistView', 'FavoriteView', 'PlayView']
