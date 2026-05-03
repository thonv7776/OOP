"""
Track Model
Represents a single track in the library.
Data representation only - no business logic.
"""


class Track:
    """Model representing a track in the music library."""

    def __init__(self, track_id, name, artist, rating=0, play_count=0):
        """
        Initialize a Track object.
        
        Args:
            track_id (int): Unique identifier for the track
            name (str): Track name/title
            artist (str): Artist name
            rating (int): Rating from 0-5 (default: 0)
            play_count (int): Number of times played (default: 0)
        """
        self.track_id = track_id
        self.name = name
        self.artist = artist
        self.rating = rating
        self.play_count = play_count

    def __str__(self):
        """String representation of track."""
        return f"{self.track_id}: {self.name} - {self.artist}"

    def __repr__(self):
        """Developer-friendly representation."""
        return (f"Track(id={self.track_id}, name='{self.name}', "
                f"artist='{self.artist}', rating={self.rating}, "
                f"play_count={self.play_count})")

    def get_info(self):
        """Get formatted track information."""
        stars = "*" * self.rating
        return f"{self.name} - {self.artist} {stars}"

    def to_dict(self):
        """Convert track to dictionary for easy serialization."""
        return {
            'track_id': self.track_id,
            'name': self.name,
            'artist': self.artist,
            'rating': self.rating,
            'play_count': self.play_count
        }
