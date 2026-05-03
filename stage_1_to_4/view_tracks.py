import tkinter as tk #import tkinter to create GUI and name it tk
import tkinter.scrolledtext as tkst #import scrollable text arena module as tkst


import track_library as lib #import the local track_library
import font_manager as fonts #import the local font_manager


def set_text(text_area, content): #Define a function to update text in text area
    text_area.delete("1.0", tk.END) #Clear existing text from the start (1.0) to the end
    text_area.insert(1.0, content) #insert new content at beginning (1.0)


class TrackViewer(): #Define main class for track viewer interface
    def __init__(self, window): #constructor to initialize the GUI and its components
        window.geometry("750x350") #window ratio
        window.title("View Tracks") #Set text displayed in window title bar

        list_tracks_btn = tk.Button(window, text="List All Tracks", command=self.list_tracks_clicked) #Create "List All Tracks" button
        list_tracks_btn.grid(row=0, column=0, padx=10, pady=10) #place button at row 0, column 0

        enter_lbl = tk.Label(window, text="Enter Track Number") #create label for track number
        enter_lbl.grid(row=0, column=1, padx=10, pady=10) #place label at row 0, column 1

        self.input_txt = tk.Entry(window, width=3) #create user input textbox
        self.input_txt.grid(row=0, column=2, padx=10, pady=10) #place input textbox at row 0, column 2

        check_track_btn = tk.Button(window, text="View Track", command=self.view_tracks_clicked) #create view track button
        check_track_btn.grid(row=0, column=3, padx=10, pady=10) #place view track button at row 0, column 3

        self.list_txt = tkst.ScrolledText(window, width=48, height=12, wrap="none") #create a scrolled text area to display track information
        self.list_txt.grid(row=1, column=0, columnspan=3, sticky="W", padx=10, pady=10) #place text area at row 1, spanning 3 columns, aligned West (left)

        self.track_txt = tk.Text(window, width=24, height=4, wrap="none") #create a text area to display track details
        self.track_txt.grid(row=1, column=3, sticky="NW", padx=10, pady=10) #place the text area at row 1, column 3, aligned North-West

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10)) #create a label to display status messages or errors
        self.status_lbl.grid(row=2, column=0, columnspan=4, sticky="W", padx=10, pady=10) #place status label at row 2, spanning 4 columns, aligned West (left)

        self.list_tracks_clicked() #Call the list_tracks_clicked when GUI starts

    def view_tracks_clicked(self): #def function run if "View Track" button is clicked
        key = self.input_txt.get() #get the track number entered by the user from the input box
        name = lib.get_name(key) #look up the track name in the library
        if name is not None: #If the song name exist
            artist = lib.get_artist(key) #Get artist information    
            rating = lib.get_rating(key) #Get rating information
            play_count = lib.get_play_count(key) #Get play count information
            track_details = f"{name}\n{artist}\nrating: {rating}\nplays: {play_count}" #Format track info into string
            set_text(self.track_txt, track_details) #Display the formatted details in the text area
        else: #other condition
            set_text(self.track_txt, f"Track {key} not found") #Show error message in track detail area
        self.status_lbl.configure(text="View Track button was clicked!") #Update the status label to confirm the button interaction

    def list_tracks_clicked(self): #Def function run when "List All Tracks" button is clicked
        track_list = lib.list_all() #Receive formatted string of all tracks from library
        set_text(self.list_txt, track_list) #Show the list of tracks in scrolled text area
        self.status_lbl.configure(text="List Tracks button was clicked!") #Update status label to confirm action

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    TrackViewer(window)     # open the TrackViewer GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
