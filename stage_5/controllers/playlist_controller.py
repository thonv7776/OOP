"""
Playlist Controller
Handles all business logic related to playlists.
Validates input and orchestrates between View and Database layers.
"""

from db import db_function


class PlaylistController:
    """Manages playlist-related business logic and validation."""

    # ========================================================================
    # VALIDATION METHODS
    # ========================================================================

    @staticmethod
    def validate_playlist_id(playlist_id):
        """
        Validate playlist ID format.
        
        Args:
            playlist_id (str): Playlist ID to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not playlist_id:
            return False, "Playlist ID cannot be empty"
        
        try:
            playlist_id_int = int(playlist_id)
            if playlist_id_int <= 0:
                return False, "Playlist ID must be a positive number"
            return True, ""
        except ValueError:
            return False, "Playlist ID must be a valid number"

    @staticmethod
    def validate_playlist_name(name):
        """
        Validate playlist name.
        
        Args:
            name (str): Playlist name to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Playlist name cannot be empty"
        if len(name) > 255:
            return False, "Playlist name is too long (max 255 characters)"
        return True, ""

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

    # ========================================================================
    # PLAYLIST RETRIEVAL METHODS
    # ========================================================================

    @staticmethod
    def get_all_playlists():
        """
        Get all playlists from database.
        
        Returns:
            list: List of Playlist objects
        """
        return db_function.get_all_playlists()

    @staticmethod
    def get_playlist_by_id(playlist_id):
        """
        Get a specific playlist by ID with validation.
        
        Args:
            playlist_id (str): Playlist ID
            
        Returns:
            tuple: (playlist_object, error_message) or (None, error_message) if invalid
        """
        is_valid, error_msg = PlaylistController.validate_playlist_id(playlist_id)
        if not is_valid:
            return None, error_msg

        playlist = db_function.get_playlist_by_id(int(playlist_id))
        if playlist is None:
            return None, f"Playlist {playlist_id} not found in database"
        return playlist, ""

    # ========================================================================
    # PLAYLIST MODIFICATION METHODS
    # ========================================================================

    @staticmethod
    def create_playlist(name):
        """
        Create a new playlist with validation.
        
        Args:
            name (str): Playlist name
            
        Returns:
            tuple: (playlist_id, error_message) or (None, error_message) if invalid
        """
        # Validate input
        is_valid, error_msg = PlaylistController.validate_playlist_name(name)
        if not is_valid:
            return None, error_msg

        # Create playlist
        playlist_id = db_function.insert_playlist(name.strip())
        if playlist_id is None:
            return None, "Failed to create playlist in database"

        return playlist_id, ""

    @staticmethod
    def add_track_to_playlist(playlist_id, track_id):
        """
        Add a track to a playlist with validation.
        
        Args:
            playlist_id (str): Playlist ID
            track_id (str): Track ID to add
            
        Returns:
            tuple: (success, error_message)
        """
        # Validate inputs
        is_valid, error_msg = PlaylistController.validate_playlist_id(playlist_id)
        if not is_valid:
            return False, error_msg

        is_valid, error_msg = PlaylistController.validate_track_id(track_id)
        if not is_valid:
            return False, error_msg

        playlist_id_int = int(playlist_id)
        track_id_int = int(track_id)

        # Check if playlist exists
        playlist = db_function.get_playlist_by_id(playlist_id_int)
        if playlist is None:
            return False, f"Playlist {playlist_id} not found"

        # Check if track exists
        track = db_function.get_track_by_id(track_id_int)
        if track is None:
            return False, f"Track {track_id} not found"

        # Check if track is already in playlist
        if any(t.track_id == track_id_int for t in playlist.tracks):
            return False, f"Track {track_id} is already in this playlist"

        # Add track to playlist
        success = db_function.add_track_to_playlist(playlist_id_int, track_id_int)
        if not success:
            return False, "Failed to add track to playlist"

        return True, ""

    @staticmethod
    def remove_track_from_playlist(playlist_id, track_id):
        """
        Remove a track from a playlist with validation.
        
        Args:
            playlist_id (str): Playlist ID
            track_id (str): Track ID to remove
            
        Returns:
            tuple: (success, error_message)
        """
        # Validate inputs
        is_valid, error_msg = PlaylistController.validate_playlist_id(playlist_id)
        if not is_valid:
            return False, error_msg

        is_valid, error_msg = PlaylistController.validate_track_id(track_id)
        if not is_valid:
            return False, error_msg

        playlist_id_int = int(playlist_id)
        track_id_int = int(track_id)

        # Check if playlist exists
        playlist = db_function.get_playlist_by_id(playlist_id_int)
        if playlist is None:
            return False, f"Playlist {playlist_id} not found"

        # Check if track is in playlist
        if not any(t.track_id == track_id_int for t in playlist.tracks):
            return False, f"Track {track_id} is not in this playlist"

        # Remove track from playlist
        success = db_function.remove_track_from_playlist(playlist_id_int, track_id_int)
        if not success:
            return False, "Failed to remove track from playlist"

        return True, ""

    @staticmethod
    def delete_playlist(playlist_id):
        """
        Delete a playlist with validation.
        
        Args:
            playlist_id (str): Playlist ID
            
        Returns:
            tuple: (success, error_message)
        """
        # Validate input
        is_valid, error_msg = PlaylistController.validate_playlist_id(playlist_id)
        if not is_valid:
            return False, error_msg

        playlist_id_int = int(playlist_id)

        # Check if playlist exists
        playlist = db_function.get_playlist_by_id(playlist_id_int)
        if playlist is None:
            return False, f"Playlist {playlist_id} not found"

        # Delete playlist
        success = db_function.delete_playlist(playlist_id_int)
        if not success:
            return False, "Failed to delete playlist"

        return True, ""

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    @staticmethod
    def format_playlist_info(playlist):
        """
        Format playlist information for display.
        
        Args:
            playlist (Playlist): Playlist object
            
        Returns:
            str: Formatted playlist information
        """
        if playlist is None:
            return ""
        
        return (f"ID: {playlist.playlist_id}\n"
                f"Name: {playlist.playlist_name}\n"
                f"Tracks: {len(playlist.tracks)}")

    @staticmethod
    def format_playlist_list(playlists):
        """
        Format list of playlists for display.
        
        Args:
            playlists (list): List of Playlist objects
            
        Returns:
            str: Formatted playlist list
        """
        if not playlists:
            return "No playlists found"

        output = ""
        for playlist in playlists:
            output += f"{playlist.playlist_id:3d}. {playlist.playlist_name:40s} ({len(playlist.tracks)} tracks)\n"
        return output
