"""
Favorite View
UI for managing favorite tracks.
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from db import db_function
from controllers.track_controller import TrackController


class FavoriteView:
    """View for displaying and managing favorite tracks."""

    def __init__(self, parent):
        """
        Initialize favorite view in parent frame.
        
        Args:
            parent (tk.Frame): Parent frame
        """
        self.parent = parent
        self.controller = TrackController()
        self._create_layout()
        self._load_favorites()

    def _create_layout(self):
        """Create the favorite view layout."""
        # ====================================================================
        # TITLE
        # ====================================================================
        title_label = tk.Label(
            self.parent,
            text="Favorite Tracks ⭐",
            font=("Helvetica", 16, "bold"),
            bg="lightgray"
        )
        title_label.pack(pady=10)

        # ====================================================================
        # CONTROL PANEL (Top)
        # ====================================================================
        control_frame = tk.Frame(self.parent, bg="lightgray")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(control_frame, text="Track ID:", bg="lightgray").pack(side=tk.LEFT, padx=5)
        self.track_id_entry = tk.Entry(control_frame, width=5)
        self.track_id_entry.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(
            control_frame,
            text="Add to Favorites",
            command=self._on_add_favorite_clicked
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(
            control_frame,
            text="Refresh",
            command=self._load_favorites
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # ====================================================================
        # CONTENT AREA (Main display)
        # ====================================================================
        content_frame = tk.Frame(self.parent, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Favorite list (left side)
        list_label = tk.Label(content_frame, text="My Favorites", bg="white", font=("Helvetica", 12, "bold"))
        list_label.pack(anchor="w", padx=10, pady=5)

        self.favorites_listbox = tk.Listbox(content_frame, height=15, width=50)
        self.favorites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(content_frame, command=self.favorites_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.favorites_listbox.config(yscrollcommand=scrollbar.set)

        # Track details (right side)
        details_label = tk.Label(content_frame, text="Track Details", bg="white", font=("Helvetica", 12, "bold"))
        details_label.pack(anchor="w", padx=10, pady=5)

        self.details_text = tkst.ScrolledText(content_frame, width=30, height=15, wrap=tk.WORD)
        self.details_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ====================================================================
        # ACTION BUTTONS (Bottom)
        # ====================================================================
        button_frame = tk.Frame(self.parent, bg="lightgray")
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        remove_btn = tk.Button(
            button_frame,
            text="Remove from Favorites",
            command=self._on_remove_favorite_clicked
        )
        remove_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self.parent, text="", bg="lightgray", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

    # ========================================================================
    # DATA LOADING METHODS
    # ========================================================================

    def _load_favorites(self):
        """Load all favorite tracks and display in listbox."""
        self.favorites_listbox.delete(0, tk.END)
        favorites = db_function.get_all_favorites()
        
        for track in favorites:
            stars = "*" * track.rating
            display_text = f"{track.track_id}. {track.name} - {track.artist} {stars}"
            self.favorites_listbox.insert(tk.END, display_text)
        
        self.status_label.config(text=f"Loaded {len(favorites)} favorite tracks")

    # ========================================================================
    # USER INTERACTION METHODS
    # ========================================================================

    def _on_add_favorite_clicked(self):
        """Handle 'Add to Favorites' button click."""
        track_id = self.track_id_entry.get()
        
        if not track_id:
            messagebox.showerror("Error", "Please enter a track ID")
            return

        try:
            track_id_int = int(track_id)
        except ValueError:
            messagebox.showerror("Error", "Track ID must be a valid number")
            return

        # Check if track exists
        track = db_function.get_track_by_id(track_id_int)
        if track is None:
            messagebox.showerror("Error", f"Track {track_id} not found")
            return

        # Check if already in favorites
        if db_function.is_favorite(track_id_int):
            messagebox.showinfo("Info", "Track is already in favorites")
            return

        # Add to favorites
        success = db_function.add_to_favorites(track_id_int)
        if success:
            messagebox.showinfo("Success", f"Track {track.name} added to favorites")
            self._load_favorites()
        else:
            messagebox.showerror("Error", "Failed to add track to favorites")

    def _on_remove_favorite_clicked(self):
        """Handle 'Remove from Favorites' button click."""
        selection = self.favorites_listbox.curselection()
        
        if not selection:
            messagebox.showerror("Error", "Please select a favorite track")
            return

        item = self.favorites_listbox.get(selection[0])
        track_id = item.split(".")[0].strip()

        if messagebox.askyesno("Confirm", "Remove from favorites?"):
            success = db_function.remove_from_favorites(int(track_id))
            if success:
                messagebox.showinfo("Success", f"Track {track_id} removed from favorites")
                self._load_favorites()
            else:
                messagebox.showerror("Error", "Failed to remove from favorites")
