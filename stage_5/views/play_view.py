"""
Play View
UI for playing tracks and managing playback.
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from db import db_function
from controllers.track_controller import TrackController


class PlayView:
    """View for playing and managing track playback."""

    def __init__(self, parent):
        """
        Initialize play view in parent frame.
        
        Args:
            parent (tk.Frame): Parent frame
        """
        self.parent = parent
        self.controller = TrackController()
        self.current_track = None
        self.is_playing = False
        self._create_layout()
        self._load_tracks()

    def _create_layout(self):
        """Create the play view layout."""
        # ====================================================================
        # TITLE
        # ====================================================================
        title_label = tk.Label(
            self.parent,
            text="Player ▶",
            font=("Helvetica", 16, "bold"),
            bg="lightgray"
        )
        title_label.pack(pady=10)

        # ====================================================================
        # PLAYER DISPLAY (Center)
        # ====================================================================
        player_frame = tk.Frame(self.parent, bg="white", relief=tk.SUNKEN, bd=2)
        player_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(player_frame, text="Now Playing:", bg="white", font=("Helvetica", 12)).pack(pady=10)

        self.now_playing_label = tk.Label(
            player_frame,
            text="No track selected",
            bg="white",
            font=("Helvetica", 14, "bold"),
            wraplength=400
        )
        self.now_playing_label.pack(pady=10)

        # Track details
        self.details_text = tkst.ScrolledText(player_frame, width=60, height=6, wrap=tk.WORD)
        self.details_text.pack(padx=10, pady=10)

        # ====================================================================
        # CONTROL BUTTONS (Player controls)
        # ====================================================================
        control_frame = tk.Frame(self.parent, bg="lightgray")
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        play_btn = tk.Button(
            control_frame,
            text="▶ Play",
            width=10,
            command=self._on_play_clicked
        )
        play_btn.pack(side=tk.LEFT, padx=5)

        stop_btn = tk.Button(
            control_frame,
            text="⏹ Stop",
            width=10,
            command=self._on_stop_clicked
        )
        stop_btn.pack(side=tk.LEFT, padx=5)

        next_btn = tk.Button(
            control_frame,
            text="⏭ Next",
            width=10,
            command=self._on_next_clicked
        )
        next_btn.pack(side=tk.LEFT, padx=5)

        # ====================================================================
        # TRACK SELECTION
        # ====================================================================
        selection_frame = tk.Frame(self.parent, bg="lightgray")
        selection_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(selection_frame, text="Select Track by ID:", bg="lightgray").pack(side=tk.LEFT, padx=5)
        self.track_id_entry = tk.Entry(selection_frame, width=5)
        self.track_id_entry.pack(side=tk.LEFT, padx=5)

        select_btn = tk.Button(
            selection_frame,
            text="Select",
            command=self._on_select_track_clicked
        )
        select_btn.pack(side=tk.LEFT, padx=5)

        # ====================================================================
        # STATUS
        # ====================================================================
        self.status_label = tk.Label(self.parent, text="Ready", bg="lightgray", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

    # ========================================================================
    # DATA LOADING METHODS
    # ========================================================================

    def _load_tracks(self):
        """Load all tracks (for potential future playlist display)."""
        self.tracks = self.controller.get_all_tracks()

    # ========================================================================
    # PLAYBACK METHODS
    # ========================================================================

    def _display_track(self, track):
        """
        Display track information in player.
        
        Args:
            track (Track): Track object to display
        """
        if track is None:
            self.now_playing_label.config(text="No track selected")
            self.details_text.delete("1.0", tk.END)
            return

        self.current_track = track
        self.now_playing_label.config(text=f"{track.name}\nby {track.artist}")
        
        info = self.controller.format_track_info(track)
        self.details_text.delete("1.0", tk.END)
        self.details_text.insert("1.0", info)

    # ========================================================================
    # USER INTERACTION METHODS
    # ========================================================================

    def _on_select_track_clicked(self):
        """Handle 'Select' button click."""
        track_id = self.track_id_entry.get()
        track, error = self.controller.get_track_by_id(track_id)
        
        if error:
            messagebox.showerror("Error", error)
        else:
            self._display_track(track)
            self.status_label.config(text=f"Selected track {track_id}")

    def _on_play_clicked(self):
        """Handle 'Play' button click."""
        if self.current_track is None:
            messagebox.showerror("Error", "Please select a track first")
            return

        # Increment play count
        success, error = self.controller.increment_track_play_count(self.current_track.track_id)
        
        if success:
            self.is_playing = True
            self.status_label.config(text=f"▶ Playing: {self.current_track.name}")
            messagebox.showinfo("Playing", f"Now playing:\n{self.current_track.name}\nby {self.current_track.artist}")
            
            # Reload track to show updated play count
            track = db_function.get_track_by_id(self.current_track.track_id)
            self._display_track(track)
        else:
            messagebox.showerror("Error", error)

    def _on_stop_clicked(self):
        """Handle 'Stop' button click."""
        if not self.is_playing:
            messagebox.showinfo("Info", "No track is playing")
            return

        self.is_playing = False
        self.status_label.config(text="⏹ Stopped")
        messagebox.showinfo("Stopped", "Playback stopped")

    def _on_next_clicked(self):
        """Handle 'Next' button click."""
        if self.current_track is None:
            messagebox.showerror("Error", "Please select a track first")
            return

        # Find next track
        current_index = None
        for i, track in enumerate(self.tracks):
            if track.track_id == self.current_track.track_id:
                current_index = i
                break

        if current_index is not None and current_index + 1 < len(self.tracks):
            next_track = self.tracks[current_index + 1]
            self._display_track(next_track)
            self.track_id_entry.delete(0, tk.END)
            self.track_id_entry.insert(0, str(next_track.track_id))
            self.status_label.config(text=f"Next: {next_track.name}")
        else:
            messagebox.showinfo("Info", "No more tracks available")
