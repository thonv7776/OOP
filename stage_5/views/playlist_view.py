"""
Playlist View
UI for viewing, creating, and managing playlists.
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
from controllers.playlist_controller import PlaylistController
from controllers.track_controller import TrackController


class PlaylistView:
    """View for displaying and managing playlists."""

    def __init__(self, parent):
        """
        Initialize playlist view in parent frame.
        
        Args:
            parent (tk.Frame): Parent frame
        """
        self.parent = parent
        self.playlist_controller = PlaylistController()
        self.track_controller = TrackController()
        self.current_playlist = None
        self._create_layout()
        self._load_playlists()

    def _create_layout(self):
        """Create the playlist view layout."""
        # ====================================================================
        # TITLE
        # ====================================================================
        title_label = tk.Label(
            self.parent,
            text="Playlists",
            font=("Helvetica", 16, "bold"),
            bg="lightgray"
        )
        title_label.pack(pady=10)

        # ====================================================================
        # CONTROL PANEL (Top)
        # ====================================================================
        control_frame = tk.Frame(self.parent, bg="lightgray")
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        create_btn = tk.Button(
            control_frame,
            text="Create Playlist",
            command=self._on_create_playlist_clicked
        )
        create_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(
            control_frame,
            text="Refresh",
            command=self._load_playlists
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # ====================================================================
        # CONTENT AREA (Main display)
        # ====================================================================
        content_frame = tk.Frame(self.parent, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Playlist list (left side)
        list_label = tk.Label(content_frame, text="My Playlists", bg="white", font=("Helvetica", 12, "bold"))
        list_label.pack(anchor="w", padx=10, pady=5)

        self.playlist_listbox = tk.Listbox(content_frame, height=15, width=40)
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.playlist_listbox.bind("<<ListboxSelect>>", self._on_playlist_selected)

        scrollbar = tk.Scrollbar(content_frame, command=self.playlist_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.playlist_listbox.config(yscrollcommand=scrollbar.set)

        # Playlist details (right side)
        details_label = tk.Label(content_frame, text="Playlist Tracks", bg="white", font=("Helvetica", 12, "bold"))
        details_label.pack(anchor="w", padx=10, pady=5)

        self.tracks_listbox = tk.Listbox(content_frame, height=15, width=40)
        self.tracks_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ====================================================================
        # ACTION BUTTONS (Bottom)
        # ====================================================================
        button_frame = tk.Frame(self.parent, bg="lightgray")
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        add_track_btn = tk.Button(
            button_frame,
            text="Add Track",
            command=self._on_add_track_clicked
        )
        add_track_btn.pack(side=tk.LEFT, padx=5)

        remove_track_btn = tk.Button(
            button_frame,
            text="Remove Track",
            command=self._on_remove_track_clicked
        )
        remove_track_btn.pack(side=tk.LEFT, padx=5)

        delete_playlist_btn = tk.Button(
            button_frame,
            text="Delete Playlist",
            command=self._on_delete_playlist_clicked
        )
        delete_playlist_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self.parent, text="", bg="lightgray", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

    # ========================================================================
    # DATA LOADING METHODS
    # ========================================================================

    def _load_playlists(self):
        """Load all playlists and display in listbox."""
        self.playlist_listbox.delete(0, tk.END)
        playlists = self.playlist_controller.get_all_playlists()
        
        for playlist in playlists:
            display_text = f"{playlist.playlist_id}. {playlist.playlist_name}"
            self.playlist_listbox.insert(tk.END, display_text)
        
        self.status_label.config(text=f"Loaded {len(playlists)} playlists")

    def _load_playlist_tracks(self, playlist_id):
        """Load tracks for a specific playlist."""
        self.tracks_listbox.delete(0, tk.END)
        playlist, error = self.playlist_controller.get_playlist_by_id(str(playlist_id))
        
        if error:
            messagebox.showerror("Error", error)
        else:
            self.current_playlist = playlist
            for track in playlist.tracks:
                display_text = f"{track.track_id}. {track.name} - {track.artist}"
                self.tracks_listbox.insert(tk.END, display_text)

    # ========================================================================
    # USER INTERACTION METHODS
    # ========================================================================

    def _on_playlist_selected(self, event):
        """Handle playlist selection in listbox."""
        selection = self.playlist_listbox.curselection()
        if not selection:
            return
        
        item = self.playlist_listbox.get(selection[0])
        playlist_id = item.split(".")[0].strip()
        self._load_playlist_tracks(int(playlist_id))

    def _on_create_playlist_clicked(self):
        """Handle 'Create Playlist' button click."""
        name = simpledialog.askstring("Create Playlist", "Enter playlist name:")
        
        if name:
            playlist_id, error = self.playlist_controller.create_playlist(name)
            if error:
                messagebox.showerror("Error", error)
            else:
                messagebox.showinfo("Success", f"Playlist created with ID {playlist_id}")
                self._load_playlists()

    def _on_add_track_clicked(self):
        """Handle 'Add Track' button click."""
        if not self.current_playlist:
            messagebox.showerror("Error", "Please select a playlist first")
            return

        track_id = simpledialog.askstring("Add Track", "Enter track ID:")
        if track_id:
            success, error = self.playlist_controller.add_track_to_playlist(
                str(self.current_playlist.playlist_id),
                track_id
            )
            
            if success:
                messagebox.showinfo("Success", f"Track {track_id} added to playlist")
                self._load_playlist_tracks(self.current_playlist.playlist_id)
            else:
                messagebox.showerror("Error", error)

    def _on_remove_track_clicked(self):
        """Handle 'Remove Track' button click."""
        if not self.current_playlist:
            messagebox.showerror("Error", "Please select a playlist first")
            return

        selection = self.tracks_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a track to remove")
            return

        item = self.tracks_listbox.get(selection[0])
        track_id = item.split(".")[0].strip()

        success, error = self.playlist_controller.remove_track_from_playlist(
            str(self.current_playlist.playlist_id),
            track_id
        )
        
        if success:
            messagebox.showinfo("Success", f"Track {track_id} removed from playlist")
            self._load_playlist_tracks(self.current_playlist.playlist_id)
        else:
            messagebox.showerror("Error", error)

    def _on_delete_playlist_clicked(self):
        """Handle 'Delete Playlist' button click."""
        if not self.current_playlist:
            messagebox.showerror("Error", "Please select a playlist first")
            return

        if messagebox.askyesno("Confirm", f"Delete playlist '{self.current_playlist.playlist_name}'?"):
            success, error = self.playlist_controller.delete_playlist(str(self.current_playlist.playlist_id))
            
            if success:
                messagebox.showinfo("Success", "Playlist deleted")
                self._load_playlists()
                self.tracks_listbox.delete(0, tk.END)
            else:
                messagebox.showerror("Error", error)
