"""
Track View
UI for viewing, adding, updating, and managing tracks.
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.scrolledtext as tkst
from controllers.track_controller import TrackController


class TrackView:
    """View for displaying and managing tracks."""

    def __init__(self, parent):
        """
        Initialize track view in parent frame.
        
        Args:
            parent (tk.Frame): Parent frame
        """
        self.parent = parent
        self.controller = TrackController()
        self._create_layout()
        self._load_tracks()

    def _create_layout(self):
        """Create the track view layout."""
        # ====================================================================
        # TITLE
        # ====================================================================
        title_label = tk.Label(
            self.parent,
            text="Track Library",
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

        view_btn = tk.Button(
            control_frame,
            text="View Track",
            command=self._on_view_track_clicked
        )
        view_btn.pack(side=tk.LEFT, padx=5)

        add_btn = tk.Button(
            control_frame,
            text="Add Track",
            command=self._on_add_track_clicked,
            bg="lightgreen"
        )
        add_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = tk.Button(
            control_frame,
            text="Refresh List",
            command=self._load_tracks
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)

        # ====================================================================
        # CONTENT AREA (Main display)
        # ====================================================================
        content_frame = tk.Frame(self.parent, bg="white")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Track list (left side)
        list_label = tk.Label(content_frame, text="All Tracks", bg="white", font=("Helvetica", 12, "bold"))
        list_label.pack(anchor="w", padx=10, pady=5)

        self.track_listbox = tk.Listbox(content_frame, height=15, width=50)
        self.track_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(content_frame, command=self.track_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.track_listbox.config(yscrollcommand=scrollbar.set)

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

        update_rating_btn = tk.Button(
            button_frame,
            text="Update Rating",
            command=self._on_update_rating_clicked
        )
        update_rating_btn.pack(side=tk.LEFT, padx=5)

        delete_btn = tk.Button(
            button_frame,
            text="Delete Track",
            command=self._on_delete_track_clicked
        )
        delete_btn.pack(side=tk.LEFT, padx=5)

        # Status label
        self.status_label = tk.Label(self.parent, text="", bg="lightgray", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

    # ========================================================================
    # DATA LOADING METHODS
    # ========================================================================

    def _load_tracks(self):
        """Load all tracks and display in listbox."""
        self.track_listbox.delete(0, tk.END)
        tracks = self.controller.get_all_tracks()
        
        for track in tracks:
            stars = "*" * track.rating
            display_text = f"{track.track_id}. {track.name} - {track.artist} {stars}"
            self.track_listbox.insert(tk.END, display_text)
        
        self.status_label.config(text=f"Loaded {len(tracks)} tracks")

    # ========================================================================
    # USER INTERACTION METHODS
    # ========================================================================

    def _on_view_track_clicked(self):
        """Handle 'View Track' button click."""
        track_id = self.track_id_entry.get()
        track, error = self.controller.get_track_by_id(track_id)
        
        if error:
            messagebox.showerror("Error", error)
            self.details_text.delete("1.0", tk.END)
        else:
            info = self.controller.format_track_info(track)
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert("1.0", info)
            self.status_label.config(text=f"Viewing track {track_id}")

    def _on_add_track_clicked(self):
        """Handle 'Add Track' button click - open dialog to add new track."""
        # Create dialog window
        dialog = tk.Toplevel(self.parent)
        dialog.title("Add New Track")
        dialog.geometry("300x250")

        # ====================================================================
        # Track Name Input
        # ====================================================================
        tk.Label(dialog, text="Track Name:", font=("Helvetica", 10)).pack(pady=5)
        name_entry = tk.Entry(dialog, width=30)
        name_entry.pack(pady=5)

        # ====================================================================
        # Artist Name Input
        # ====================================================================
        tk.Label(dialog, text="Artist Name:", font=("Helvetica", 10)).pack(pady=5)
        artist_entry = tk.Entry(dialog, width=30)
        artist_entry.pack(pady=5)

        # ====================================================================
        # Rating Input
        # ====================================================================
        tk.Label(dialog, text="Rating (0-5):", font=("Helvetica", 10)).pack(pady=5)
        rating_entry = tk.Entry(dialog, width=30)
        rating_entry.insert(0, "0")  # Default rating = 0
        rating_entry.pack(pady=5)

        # ====================================================================
        # Action Buttons
        # ====================================================================
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=15)

        def confirm_add():
            """Validate and add track."""
            name = name_entry.get()
            artist = artist_entry.get()
            rating = rating_entry.get()

            # Call controller to validate and add
            track_id, error = self.controller.add_track(name, artist, rating)

            if error:
                messagebox.showerror("Error", error)
            else:
                messagebox.showinfo(
                    "Success",
                    f"Track added successfully!\nTrack ID: {track_id}"
                )
                self._load_tracks()  # Refresh list
                dialog.destroy()

        add_confirm_btn = tk.Button(
            button_frame,
            text="Add",
            command=confirm_add,
            width=10
        )
        add_confirm_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            command=dialog.destroy,
            width=10
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

    def _on_update_rating_clicked(self):
        """Handle 'Update Rating' button click."""
        track_id = self.track_id_entry.get()
        
        if not track_id:
            messagebox.showerror("Error", "Please enter a track ID")
            return

        # Create rating dialog
        dialog = tk.Toplevel(self.parent)
        dialog.title("Update Rating")
        dialog.geometry("300x150")

        tk.Label(dialog, text="Enter new rating (0-5):").pack(pady=10)
        
        rating_entry = tk.Entry(dialog)
        rating_entry.pack(pady=5)

        def confirm_update():
            rating = rating_entry.get()
            success, error = self.controller.update_track_rating(track_id, rating)
            
            if success:
                messagebox.showinfo("Success", f"Rating updated to {rating}")
                self._load_tracks()
                dialog.destroy()
            else:
                messagebox.showerror("Error", error)

        update_btn = tk.Button(dialog, text="Update", command=confirm_update)
        update_btn.pack(pady=10)

    def _on_delete_track_clicked(self):
        """Handle 'Delete Track' button click."""
        track_id = self.track_id_entry.get()
        
        if not track_id:
            messagebox.showerror("Error", "Please enter a track ID")
            return

        if messagebox.askyesno("Confirm", f"Delete track {track_id}?"):
            success, error = self.controller.delete_track(track_id)
            
            if success:
                messagebox.showinfo("Success", f"Track {track_id} deleted")
                self._load_tracks()
            else:
                messagebox.showerror("Error", error)
