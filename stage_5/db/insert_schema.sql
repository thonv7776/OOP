-- COMP1752 Jukebox Coursework - Database Schema
-- MySQL Database Setup
-- Execute this file to create the database schema

-- Create Database
CREATE DATABASE IF NOT EXISTS jukebox_db;
USE jukebox_db;

-- ============================================================================
-- Table: tracks
-- Description: Stores all track information in the library
-- ============================================================================
CREATE TABLE IF NOT EXISTS tracks (
    track_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    rating INT DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    play_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: playlists
-- Description: Stores playlist information created by users
-- ============================================================================
CREATE TABLE IF NOT EXISTS playlists (
    playlist_id INT PRIMARY KEY AUTO_INCREMENT,
    playlist_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- Table: playlist_tracks
-- Description: Junction table to store tracks in playlists (many-to-many)
-- ============================================================================
CREATE TABLE IF NOT EXISTS playlist_tracks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    playlist_id INT NOT NULL,
    track_id INT NOT NULL,
    position INT,
    FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    UNIQUE KEY unique_playlist_track (playlist_id, track_id)
);

-- ============================================================================
-- Table: favorites
-- Description: Stores user's favorite tracks
-- ============================================================================
CREATE TABLE IF NOT EXISTS favorites (
    favorite_id INT PRIMARY KEY AUTO_INCREMENT,
    track_id INT NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (track_id) REFERENCES tracks(track_id) ON DELETE CASCADE,
    UNIQUE KEY unique_favorite_track (track_id)
);

-- ============================================================================
-- Sample Data: Insert initial tracks from track_library.py
-- ============================================================================
INSERT INTO tracks (name, artist, rating, play_count) VALUES
('What a Wonderful World', 'Louis Armstrong', 5, 0),
('Here Comes the Sun', 'The Beatles', 5, 0),
('Count on Me', 'Bruno Mars', 3, 0),
('Three Little Birds', 'Bob Marley', 1, 0),
('You''ve Got a Friend', 'James Taylor', 3, 0);

-- ============================================================================
-- Indexes for Performance
-- ============================================================================
CREATE INDEX idx_track_artist ON tracks(artist);
CREATE INDEX idx_track_rating ON tracks(rating);
CREATE INDEX idx_playlist_name ON playlists(playlist_name);
CREATE INDEX idx_favorite_track ON favorites(track_id);

-- ============================================================================
-- End of Database Schema
-- ============================================================================
