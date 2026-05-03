"""
Playlist Model
Represents a collection of tracks.
Data representation only - no business logic.
"""


class Playlist:
    """Model representing a playlist."""

    def __init__(self, playlist_id, playlist_name, tracks=None):
        """
        Initialize a Playlist object.
        
        Args:
            playlist_id (int): Unique identifier for the playlist
            playlist_name (str): Name of the playlist
            tracks (list): List of Track objects (default: empty list)
        """
        self.playlist_id = playlist_id
        self.playlist_name = playlist_name
        self.tracks = tracks if tracks is not None else []

    def __str__(self):
        """String representation of playlist."""
        return f"{self.playlist_name} ({len(self.tracks)} tracks)"

    def __repr__(self):
        """Developer-friendly representation."""
        return f"Playlist(id={self.playlist_id}, name='{self.playlist_name}', tracks={len(self.tracks)})"

    def get_track_count(self):
        """Get number of tracks in playlist."""
        return len(self.tracks)

    def to_dict(self):
        """Convert playlist to dictionary for easy serialization."""
        return {
            'playlist_id': self.playlist_id,
            'playlist_name': self.playlist_name,
            'track_count': len(self.tracks)
        }
