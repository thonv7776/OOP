"""
Database Functions
Contains all SQL queries and database operations.
All queries are parameterized to prevent SQL injection.
"""

from db.db_connection import db
from models.track import Track
from models.playlist import Playlist


# ============================================================================
# TRACK FUNCTIONS
# ============================================================================

def get_all_tracks():
    """
    Retrieve all tracks from database.
    
    Returns:
        list: List of Track objects
    """
    try:
        cursor = db.get_cursor()
        query = "SELECT track_id, name, artist, rating, play_count FROM tracks ORDER BY track_id"
        cursor.execute(query)
        results = cursor.fetchall()
        db.close_cursor(cursor)

        tracks = [Track(
            track_id=row['track_id'],
            name=row['name'],
            artist=row['artist'],
            rating=row['rating'],
            play_count=row['play_count']
        ) for row in results]
        
        return tracks
    except Exception as e:
        print(f"Error retrieving tracks: {e}")
        return []


def get_track_by_id(track_id):
    """
    Retrieve a specific track by ID.
    
    Args:
        track_id (int): Track identifier
        
    Returns:
        Track: Track object or None if not found
    """
    try:
        cursor = db.get_cursor()
        query = "SELECT track_id, name, artist, rating, play_count FROM tracks WHERE track_id = %s"
        cursor.execute(query, (track_id,))
        result = cursor.fetchone()
        db.close_cursor(cursor)

        if result:
            return Track(
                track_id=result['track_id'],
                name=result['name'],
                artist=result['artist'],
                rating=result['rating'],
                play_count=result['play_count']
            )
        return None
    except Exception as e:
        print(f"Error retrieving track {track_id}: {e}")
        return None


def insert_track(name, artist, rating=0):
    """
    Insert a new track into database.
    
    Args:
        name (str): Track name
        artist (str): Artist name
        rating (int): Rating 0-5 (default: 0)
        
    Returns:
        int: New track ID or None if failed
    """
    try:
        cursor = db.get_cursor()
        query = "INSERT INTO tracks (name, artist, rating, play_count) VALUES (%s, %s, %s, 0)"
        cursor.execute(query, (name, artist, rating))
        db.commit()
        track_id = cursor.lastrowid
        db.close_cursor(cursor)
        print(f"✓ Track inserted with ID: {track_id}")
        return track_id
    except Exception as e:
        db.rollback()
        print(f"Error inserting track: {e}")
        return None


def update_track_rating(track_id, rating):
    """
    Update track rating.
    
    Args:
        track_id (int): Track identifier
        rating (int): New rating (0-5)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "UPDATE tracks SET rating = %s WHERE track_id = %s"
        cursor.execute(query, (rating, track_id))
        db.commit()
        db.close_cursor(cursor)
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"Error updating rating: {e}")
        return False


def increment_play_count(track_id):
    """
    Increment play count for a track.
    
    Args:
        track_id (int): Track identifier
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "UPDATE tracks SET play_count = play_count + 1 WHERE track_id = %s"
        cursor.execute(query, (track_id,))
        db.commit()
        db.close_cursor(cursor)
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"Error incrementing play count: {e}")
        return False


def delete_track(track_id):
    """
    Delete a track from database.
    
    Args:
        track_id (int): Track identifier
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "DELETE FROM tracks WHERE track_id = %s"
        cursor.execute(query, (track_id,))
        db.commit()
        db.close_cursor(cursor)
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"Error deleting track: {e}")
        return False


# ============================================================================
# PLAYLIST FUNCTIONS
# ============================================================================

def get_all_playlists():
    """
    Retrieve all playlists from database.
    
    Returns:
        list: List of Playlist objects
    """
    try:
        cursor = db.get_cursor()
        query = "SELECT playlist_id, playlist_name FROM playlists ORDER BY playlist_id"
        cursor.execute(query)
        results = cursor.fetchall()
        db.close_cursor(cursor)

        playlists = [Playlist(
            playlist_id=row['playlist_id'],
            playlist_name=row['playlist_name']
        ) for row in results]
        
        return playlists
    except Exception as e:
        print(f"Error retrieving playlists: {e}")
        return []


def get_playlist_by_id(playlist_id):
    """
    Retrieve a specific playlist with all its tracks.
    
    Args:
        playlist_id (int): Playlist identifier
        
    Returns:
        Playlist: Playlist object or None if not found
    """
    try:
        cursor = db.get_cursor()
        query = "SELECT playlist_id, playlist_name FROM playlists WHERE playlist_id = %s"
        cursor.execute(query, (playlist_id,))
        result = cursor.fetchone()
        
        if not result:
            db.close_cursor(cursor)
            return None

        # Get tracks in this playlist
        track_query = """
            SELECT t.track_id, t.name, t.artist, t.rating, t.play_count
            FROM tracks t
            JOIN playlist_tracks pt ON t.track_id = pt.track_id
            WHERE pt.playlist_id = %s
            ORDER BY pt.position
        """
        cursor.execute(track_query, (playlist_id,))
        track_results = cursor.fetchall()
        db.close_cursor(cursor)

        tracks = [Track(
            track_id=row['track_id'],
            name=row['name'],
            artist=row['artist'],
            rating=row['rating'],
            play_count=row['play_count']
        ) for row in track_results]

        return Playlist(
            playlist_id=result['playlist_id'],
            playlist_name=result['playlist_name'],
            tracks=tracks
        )
    except Exception as e:
        print(f"Error retrieving playlist {playlist_id}: {e}")
        return None


def insert_playlist(playlist_name):
    """
    Create a new playlist.
    
    Args:
        playlist_name (str): Name for the playlist
        
    Returns:
        int: New playlist ID or None if failed
    """
    try:
        cursor = db.get_cursor()
        query = "INSERT INTO playlists (playlist_name) VALUES (%s)"
        cursor.execute(query, (playlist_name,))
        db.commit()
        playlist_id = cursor.lastrowid
        db.close_cursor(cursor)
        print(f"✓ Playlist created with ID: {playlist_id}")
        return playlist_id
    except Exception as e:
        db.rollback()
        print(f"Error creating playlist: {e}")
        return None


def add_track_to_playlist(playlist_id, track_id, position=None):
    """
    Add a track to a playlist.
    
    Args:
        playlist_id (int): Playlist identifier
        track_id (int): Track identifier
        position (int): Position in playlist (optional)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        
        # Get next position if not specified
        if position is None:
            pos_query = "SELECT MAX(position) as max_pos FROM playlist_tracks WHERE playlist_id = %s"
            cursor.execute(pos_query, (playlist_id,))
            result = cursor.fetchone()
            position = (result['max_pos'] or 0) + 1

        query = """
            INSERT INTO playlist_tracks (playlist_id, track_id, position)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (playlist_id, track_id, position))
        db.commit()
        db.close_cursor(cursor)
        return True
    except Exception as e:
        db.rollback()
        print(f"Error adding track to playlist: {e}")
        return False


def remove_track_from_playlist(playlist_id, track_id):
    """
    Remove a track from a playlist.
    
    Args:
        playlist_id (int): Playlist identifier
        track_id (int): Track identifier
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "DELETE FROM playlist_tracks WHERE playlist_id = %s AND track_id = %s"
        cursor.execute(query, (playlist_id, track_id))
        db.commit()
        db.close_cursor(cursor)
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"Error removing track from playlist: {e}")
        return False


def delete_playlist(playlist_id):
    """
    Delete a playlist (also removes all tracks from it).
    
    Args:
        playlist_id (int): Playlist identifier
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "DELETE FROM playlists WHERE playlist_id = %s"
        cursor.execute(query, (playlist_id,))
        db.commit()
        db.close_cursor(cursor)
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"Error deleting playlist: {e}")
        return False


# ============================================================================
# FAVORITE FUNCTIONS
# ============================================================================

def get_all_favorites():
    """
    Retrieve all favorite tracks.
    
    Returns:
        list: List of Track objects marked as favorites
    """
    try:
        cursor = db.get_cursor()
        query = """
            SELECT t.track_id, t.name, t.artist, t.rating, t.play_count
            FROM tracks t
            JOIN favorites f ON t.track_id = f.track_id
            ORDER BY f.added_at DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        db.close_cursor(cursor)

        tracks = [Track(
            track_id=row['track_id'],
            name=row['name'],
            artist=row['artist'],
            rating=row['rating'],
            play_count=row['play_count']
        ) for row in results]
        
        return tracks
    except Exception as e:
        print(f"Error retrieving favorites: {e}")
        return []


def add_to_favorites(track_id):
    """
    Add a track to favorites.
    
    Args:
        track_id (int): Track identifier
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "INSERT INTO favorites (track_id) VALUES (%s)"
        cursor.execute(query, (track_id,))
        db.commit()
        db.close_cursor(cursor)
        return True
    except Exception as e:
        db.rollback()
        print(f"Error adding to favorites: {e}")
        return False


def remove_from_favorites(track_id):
    """
    Remove a track from favorites.
    
    Args:
        track_id (int): Track identifier
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "DELETE FROM favorites WHERE track_id = %s"
        cursor.execute(query, (track_id,))
        db.commit()
        db.close_cursor(cursor)
        return cursor.rowcount > 0
    except Exception as e:
        db.rollback()
        print(f"Error removing from favorites: {e}")
        return False


def is_favorite(track_id):
    """
    Check if a track is in favorites.
    
    Args:
        track_id (int): Track identifier
        
    Returns:
        bool: True if track is a favorite, False otherwise
    """
    try:
        cursor = db.get_cursor()
        query = "SELECT COUNT(*) as count FROM favorites WHERE track_id = %s"
        cursor.execute(query, (track_id,))
        result = cursor.fetchone()
        db.close_cursor(cursor)
        return result['count'] > 0
    except Exception as e:
        print(f"Error checking favorite: {e}")
        return False
