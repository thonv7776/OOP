import tkinter as tk #import tkinter to create GUI and name it tk
import tkinter.scrolledtext as tkst #import scrollable text arena module as tkst


import track_library as lib #import the local track_library
import font_manager as fonts #import the local font_manager


def set_text(text_area, content): #Define a function to update text in text area
    text_area.delete("1.0", tk.END) #Clear existing text from the start (1.0) to the end
    text_area.insert(1.0, content) #insert new content at beginning (1.0)


class CreateTrackList(): #Define main class for creating track list (playlist) interface
    def __init__(self, window): #constructor to initialize the GUI and its components
        window.geometry("750x400") #window ratio
        window.title("Create Track List") #Set text displayed in window title bar

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked) #Create "List All Tracks" button
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10) #place button at row 0, column 0

        enter_lbl = tk.Label(window, text="Enter Track Number") #create label for track number
        enter_lbl.grid(row=0, column=1, padx=10, pady=10) #place label at row 0, column 1

        self.input_txt = tk.Entry(window, width=3) #create user input textbox for track number
        self.input_txt.grid(row=0, column=2, padx=10, pady=10) #place input textbox at row 0, column 2

        add_btn = tk.Button(window, text="Add to Playlist", command=self.add_to_playlist_clicked) #create add to playlist button
        add_btn.grid(row=0, column=3, padx=10, pady=10) #place add to playlist button at row 0, column 3

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none") #create a scrolled text area to display all available tracks
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10) #place text area at row 1, spanning 3 columns, aligned West (left)

        playlist_label = tk.Label(window, text="Current Playlist") #create label for playlist display area
        playlist_label.grid(row=0, column=4, padx=10, pady=10) #place label at row 0, column 4

        self.playlist_txt = tk.Text(window, width=24, height=12, wrap="none") #create a text area to display tracks added to current playlist
        self.playlist_txt.grid(row=1, column=4, sticky="NW", padx=10, pady=10) #place playlist text area at row 1, column 4, aligned North-West

        play_btn = tk.Button(window, text="Play Playlist", command=self.play_playlist_clicked) #create play playlist button
        play_btn.grid(row=2, column=3, padx=10, pady=10) #place play playlist button at row 2, column 3

        clear_btn = tk.Button(window, text="Clear Playlist", command=self.clear_playlist_clicked) #create clear playlist button
        clear_btn.grid(row=2, column=4, padx=10, pady=10) #place clear playlist button at row 2, column 4

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10)) #create a label to display status messages or errors
        self.status_lbl.grid(row=3, column=0, columnspan=5, sticky="W", padx=10, pady=10) #place status label at row 3, spanning 5 columns, aligned West (left)

        self.playlist = [] #initialize an internal list to store track keys added to the playlist

        self.list_tracks_clicked() #Call the list_tracks_clicked when GUI starts

    def list_tracks_clicked(self): #Def function run when "List All Tracks" button is clicked
        track_list = lib.list_all() #Receive formatted string of all tracks from library
        set_text(self.list_txt, track_list) #Show the list of tracks in scrolled text area
        self.status_lbl.configure(text="Displaying all available tracks") #Update status label to confirm action

    def add_to_playlist_clicked(self): #Def function run when "Add to Playlist" button is clicked
        key = self.input_txt.get() #get the track number entered by the user from the input box
        name = lib.get_name(key) #look up the track name in the library
        if name is not None: #If the song name exist
            self.playlist.append(key) #Add the track key to the internal playlist list
            artist = lib.get_artist(key) #Get artist information
            rating = lib.get_rating(key) #Get rating information
            track_info = f"{key} {name} - {artist} {self.format_stars(rating)}\n" #Format track info for display
            self.playlist_txt.insert(tk.END, track_info) #Insert the track info at the end of the playlist text area
            self.status_lbl.configure(text=f"Track {key} added to playlist") #Update status label to confirm addition
        else: #other condition
            self.status_lbl.configure(text=f"Track {key} not found") #Show error message in status label
        self.input_txt.delete(0, tk.END) #Clear the input textbox

    def play_playlist_clicked(self): #Def function run when "Play Playlist" button is clicked
        if len(self.playlist) == 0: #If the playlist is empty
            self.status_lbl.configure(text="Playlist is empty, add tracks first") #Show error message
            return #Exit function
        
        for key in self.playlist: #Iterate through each track in the playlist
            lib.increment_play_count(key) #Increment the play count for each track
        
        self.status_lbl.configure(text=f"Playing {len(self.playlist)} tracks from playlist") #Update status label with confirmation message

    def clear_playlist_clicked(self): #Def function run when "Clear Playlist" button is clicked
        self.playlist = [] #Empty the playlist by creating new empty list
        set_text(self.playlist_txt, "") #Clear the playlist text area
        self.status_lbl.configure(text="Playlist cleared") #Update status label to confirm action

    def format_stars(self, rating): #Helper function to format rating as stars
        stars = "" #initialize empty stars string
        for i in range(rating): #loop based on rating number
            stars += "*" #add one star per rating point
        return stars #return formatted stars string

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    CreateTrackList(window) # open the CreateTrackList GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
