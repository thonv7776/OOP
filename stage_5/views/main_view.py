"""
Main View - Entry point for the Jukebox UI
Single-window integrated layout with sidebar navigation.
"""

import tkinter as tk
from tkinter import messagebox
import font_manager


class MainView:
    """Main application window with integrated UI for all features."""

    def __init__(self, root):
        """
        Initialize the main application window.
        
        Args:
            root (tk.Tk): Root Tkinter window
        """
        self.root = root
        self.root.geometry("1000x600")
        self.root.title("Jukebox Application")
        self.root.configure(bg="lightgray")

        # Configure fonts
        font_manager.configure()

        # Create main layout
        self._create_layout()

    def _create_layout(self):
        """Create the main UI layout with sidebar and content area."""
        # ====================================================================
        # SIDEBAR (Left)
        # ====================================================================
        self.sidebar_frame = tk.Frame(self.root, bg="darkgray", width=150)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)
        self.sidebar_frame.pack_propagate(False)

        sidebar_title = tk.Label(
            self.sidebar_frame,
            text="Navigation",
            bg="darkgray",
            fg="white",
            font=("Helvetica", 14, "bold")
        )
        sidebar_title.pack(pady=10)

        # Navigation buttons
        self.tracks_btn = tk.Button(
            self.sidebar_frame,
            text="📚 View Tracks",
            width=15,
            command=self._on_tracks_clicked,
            bg="white"
        )
        self.tracks_btn.pack(pady=5, padx=5)

        self.playlists_btn = tk.Button(
            self.sidebar_frame,
            text="📋 Playlists",
            width=15,
            command=self._on_playlists_clicked,
            bg="white"
        )
        self.playlists_btn.pack(pady=5, padx=5)

        self.favorites_btn = tk.Button(
            self.sidebar_frame,
            text="⭐ Favorites",
            width=15,
            command=self._on_favorites_clicked,
            bg="white"
        )
        self.favorites_btn.pack(pady=5, padx=5)

        self.play_btn = tk.Button(
            self.sidebar_frame,
            text="▶ Play",
            width=15,
            command=self._on_play_clicked,
            bg="white"
        )
        self.play_btn.pack(pady=5, padx=5)

        # ====================================================================
        # CONTENT AREA (Right)
        # ====================================================================
        self.content_frame = tk.Frame(self.root, bg="lightgray")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Welcome message
        self.welcome_label = tk.Label(
            self.content_frame,
            text="Welcome to Jukebox\nSelect an option from the sidebar",
            bg="lightgray",
            font=("Helvetica", 16)
        )
        self.welcome_label.pack(pady=50)

    # ========================================================================
    # NAVIGATION CALLBACK METHODS
    # ========================================================================

    def _on_tracks_clicked(self):
        """Handle 'View Tracks' button click."""
        self._clear_content()
        # Import here to avoid circular imports
        from views.track_view import TrackView
        TrackView(self.content_frame)

    def _on_playlists_clicked(self):
        """Handle 'Playlists' button click."""
        self._clear_content()
        from views.playlist_view import PlaylistView
        PlaylistView(self.content_frame)

    def _on_favorites_clicked(self):
        """Handle 'Favorites' button click."""
        self._clear_content()
        from views.favorite_view import FavoriteView
        FavoriteView(self.content_frame)

    def _on_play_clicked(self):
        """Handle 'Play' button click."""
        self._clear_content()
        from views.play_view import PlayView
        PlayView(self.content_frame)

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def _clear_content(self):
        """Clear all widgets from content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_success(self, message):
        """
        Show success message popup.
        
        Args:
            message (str): Success message
        """
        messagebox.showinfo("Success", message)

    def show_error(self, message):
        """
        Show error message popup.
        
        Args:
            message (str): Error message
        """
        messagebox.showerror("Error", message)

    def show_info(self, message):
        """
        Show info message popup.
        
        Args:
            message (str): Info message
        """
        messagebox.showinfo("Information", message)
