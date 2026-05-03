"""
Track Controller
Handles all business logic related to tracks.
Validates input and orchestrates between View and Database layers.
"""

from db import db_function


class TrackController:
    """Manages track-related business logic and validation."""

    # ========================================================================
    # VALIDATION METHODS
    # ========================================================================

    @staticmethod
    def validate_track_id(track_id):
        """
        Validate track ID format.
        
        Args:
            track_id (str): Track ID to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not track_id:
            return False, "Track ID cannot be empty"
        
        try:
            track_id_int = int(track_id)
            if track_id_int <= 0:
                return False, "Track ID must be a positive number"
            return True, ""
        except ValueError:
            return False, "Track ID must be a valid number"

    @staticmethod
    def validate_rating(rating):
        """
        Validate rating value.
        
        Args:
            rating (str or int): Rating to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            rating_int = int(rating)
            if rating_int < 0 or rating_int > 5:
                return False, "Rating must be between 0 and 5"
            return True, ""
        except ValueError:
            return False, "Rating must be a valid number"

    @staticmethod
    def validate_track_name(name):
        """
        Validate track name.
        
        Args:
            name (str): Track name to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Track name cannot be empty"
        if len(name) > 255:
            return False, "Track name is too long (max 255 characters)"
        return True, ""

    @staticmethod
    def validate_artist_name(artist):
        """
        Validate artist name.
        
        Args:
            artist (str): Artist name to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not artist or not artist.strip():
            return False, "Artist name cannot be empty"
        if len(artist) > 255:
            return False, "Artist name is too long (max 255 characters)"
        return True, ""

    # ========================================================================
    # TRACK RETRIEVAL METHODS
    # ========================================================================

    @staticmethod
    def get_all_tracks():
        """
        Get all tracks from database.
        
        Returns:
            list: List of Track objects
        """
        return db_function.get_all_tracks()

    @staticmethod
    def get_track_by_id(track_id):
        """
        Get a specific track by ID with validation.
        
        Args:
            track_id (str): Track ID
            
        Returns:
            tuple: (track_object, error_message) or (None, error_message) if invalid
        """
        is_valid, error_msg = TrackController.validate_track_id(track_id)
        if not is_valid:
            return None, error_msg

        track = db_function.get_track_by_id(int(track_id))
        if track is None:
            return None, f"Track {track_id} not found in database"
        return track, ""

    # ========================================================================
    # TRACK MODIFICATION METHODS
    # ========================================================================

    @staticmethod
    def add_track(name, artist, rating=0):
        """
        Add a new track with validation.
        
        Args:
            name (str): Track name
            artist (str): Artist name
            rating (int): Initial rating (default: 0)
            
        Returns:
            tuple: (track_id, error_message) or (None, error_message) if invalid
        """
        # Validate inputs
        is_valid, error_msg = TrackController.validate_track_name(name)
        if not is_valid:
            return None, error_msg

        is_valid, error_msg = TrackController.validate_artist_name(artist)
        if not is_valid:
            return None, error_msg

        is_valid, error_msg = TrackController.validate_rating(rating)
        if not is_valid:
            return None, error_msg

        # Insert track
        track_id = db_function.insert_track(name.strip(), artist.strip(), int(rating))
        if track_id is None:
            return None, "Failed to add track to database"

        return track_id, ""

    @staticmethod
    def update_track_rating(track_id, rating):
        """
        Update track rating with validation.
        
        Args:
            track_id (str): Track ID
            rating (str): New rating value
            
        Returns:
            tuple: (success, error_message)
        """
        # Validate inputs
        is_valid, error_msg = TrackController.validate_track_id(track_id)
        if not is_valid:
            return False, error_msg

        is_valid, error_msg = TrackController.validate_rating(rating)
        if not is_valid:
            return False, error_msg

        # Check if track exists
        track = db_function.get_track_by_id(int(track_id))
        if track is None:
            return False, f"Track {track_id} not found"

        # Update rating
        success = db_function.update_track_rating(int(track_id), int(rating))
        if not success:
            return False, "Failed to update track rating"

        return True, ""

    @staticmethod
    def increment_track_play_count(track_id):
        """
        Increment play count for a track.
        
        Args:
            track_id (int): Track ID
            
        Returns:
            tuple: (success, error_message)
        """
        track = db_function.get_track_by_id(track_id)
        if track is None:
            return False, f"Track {track_id} not found"

        success = db_function.increment_play_count(track_id)
        if not success:
            return False, "Failed to increment play count"

        return True, ""

    @staticmethod
    def delete_track(track_id):
        """
        Delete a track with validation.
        
        Args:
            track_id (str): Track ID
            
        Returns:
            tuple: (success, error_message)
        """
        # Validate input
        is_valid, error_msg = TrackController.validate_track_id(track_id)
        if not is_valid:
            return False, error_msg

        # Check if track exists
        track = db_function.get_track_by_id(int(track_id))
        if track is None:
            return False, f"Track {track_id} not found"

        # Delete track
        success = db_function.delete_track(int(track_id))
        if not success:
            return False, "Failed to delete track"

        return True, ""

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    @staticmethod
    def format_track_info(track):
        """
        Format track information for display.
        
        Args:
            track (Track): Track object
            
        Returns:
            str: Formatted track information
        """
        if track is None:
            return ""
        
        stars = "*" * track.rating
        return (f"ID: {track.track_id}\n"
                f"Name: {track.name}\n"
                f"Artist: {track.artist}\n"
                f"Rating: {stars} ({track.rating}/5)\n"
                f"Plays: {track.play_count}")

    @staticmethod
    def format_track_list(tracks):
        """
        Format list of tracks for display.
        
        Args:
            tracks (list): List of Track objects
            
        Returns:
            str: Formatted track list
        """
        if not tracks:
            return "No tracks found"

        output = ""
        for track in tracks:
            stars = "*" * track.rating
            output += f"{track.track_id:3d}. {track.name:30s} - {track.artist:20s} {stars}\n"
        return output
