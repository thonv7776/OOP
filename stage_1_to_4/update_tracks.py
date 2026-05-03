import tkinter as tk #import tkinter to create GUI and name it tk
import tkinter.scrolledtext as tkst #import scrollable text arena module as tkst


import track_library as lib #import the local track_library
import font_manager as fonts #import the local font_manager


def set_text(text_area, content): #Define a function to update text in text area
    text_area.delete("1.0", tk.END) #Clear existing text from the start (1.0) to the end
    text_area.insert(1.0, content) #insert new content at beginning (1.0)


class UpdateTracks(): #Define main class for updating track ratings interface
    def __init__(self, window): #constructor to initialize the GUI and its components
        window.geometry("600x350") #window ratio
        window.title("Update Tracks") #Set text displayed in window title bar

        key_lbl = tk.Label(window, text="Enter Track Number") #create label for track number
        key_lbl.grid(row=0, column=0, padx=10, pady=10) #place label at row 0, column 0

        self.key_txt = tk.Entry(window, width=3) #create user input textbox for track number
        self.key_txt.grid(row=0, column=1, padx=10, pady=10) #place input textbox at row 0, column 1

        rating_lbl = tk.Label(window, text="Enter New Rating (1-5)") #create label for new rating input
        rating_lbl.grid(row=0, column=2, padx=10, pady=10) #place label at row 0, column 2

        self.rating_txt = tk.Entry(window, width=3) #create user input textbox for new rating value
        self.rating_txt.grid(row=0, column=3, padx=10, pady=10) #place input textbox at row 0, column 3

        update_btn = tk.Button(window, text="Update Track", command=self.update_track_clicked) #create update track button
        update_btn.grid(row=0, column=4, padx=10, pady=10) #place update track button at row 0, column 4

        self.track_txt = tk.Text(window, width=70, height=8, wrap="none") #create a text area to display updated track information
        self.track_txt.grid(row=1, column=0, columnspan=5, sticky="W", padx=10, pady=10) #place text area at row 1, spanning 5 columns, aligned West (left)

        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10)) #create a label to display status messages or errors
        self.status_lbl.grid(row=2, column=0, columnspan=5, sticky="W", padx=10, pady=10) #place status label at row 2, spanning 5 columns, aligned West (left)

    def update_track_clicked(self): #Def function run when "Update Track" button is clicked
        key = self.key_txt.get() #get the track number entered by the user from the input box
        rating_str = self.rating_txt.get() #get the new rating entered by the user from the input box

        if not rating_str: #If rating input is empty
            self.status_lbl.configure(text="Please enter a rating value") #Show error message
            return #Exit function

        try: #Try to execute the following code
            new_rating = int(rating_str) #Convert the rating string to integer
        except ValueError: #If conversion fails
            self.status_lbl.configure(text="Invalid rating, please enter a number") #Show error message
            return #Exit function

        if new_rating < 1 or new_rating > 5: #If rating is outside valid range
            self.status_lbl.configure(text="Rating must be between 1 and 5") #Show error message
            return #Exit function

        name = lib.get_name(key) #look up the track name in the library
        if name is not None: #If the track exists
            lib.set_rating(key, new_rating) #Update the track rating in the library
            artist = lib.get_artist(key) #Get artist information
            rating = lib.get_rating(key) #Get updated rating information
            play_count = lib.get_play_count(key) #Get play count information
            track_details = f"Track Number: {key}\nName: {name}\nArtist: {artist}\nRating: {self.format_stars(rating)}\nPlay Count: {play_count}" #Format track info into string
            set_text(self.track_txt, track_details) #Display the formatted details in the text area
            self.status_lbl.configure(text=f"Track {key} updated successfully with {new_rating} star(s)") #Update status label with success message
        else: #other condition
            set_text(self.track_txt, f"Track {key} not found") #Show error message in track detail area
            self.status_lbl.configure(text=f"Track {key} not found") #Show error message in status label

        self.key_txt.delete(0, tk.END) #Clear the track number input box
        self.rating_txt.delete(0, tk.END) #Clear the rating input box

    def format_stars(self, rating): #Helper function to format rating as stars
        stars = "" #initialize empty stars string
        for i in range(rating): #loop based on rating number
            stars += "*" #add one star per rating point
        return stars #return formatted stars string

if __name__ == "__main__":  # only runs when this file is run as a standalone
    window = tk.Tk()        # create a TK object
    fonts.configure()       # configure the fonts
    UpdateTracks(window)    # open the UpdateTracks GUI
    window.mainloop()       # run the window main loop, reacting to button presses, etc
