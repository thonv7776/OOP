"""
Jukebox Application - Entry Point
Main application initialization and startup.

This is the entry point for the COMP1752 Jukebox coursework application.
It initializes the database connection and launches the main UI.
"""

import tkinter as tk
from db.db_connection import db
from views.main_view import MainView


def main():
    """
    Initialize and run the Jukebox application.
    
    1. Establishes database connection
    2. Creates the main window
    3. Launches the main UI
    4. Starts the event loop
    """
    # Initialize database connection
    print("Initializing Jukebox Application...")
    
    if not db.connect():
        print("ERROR: Failed to connect to database")
        print("Please ensure:")
        print("1. XAMPP MySQL is running")
        print("2. Database 'jukebox_db' exists")
        print("3. Schema has been created with insert_schema.sql")
        return

    # Create root window
    root = tk.Tk()

    # Initialize main view
    main_view = MainView(root)

    # Handle window close
    def on_closing():
        """Handle application exit."""
        db.disconnect()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Start the application
    print("✓ Application started successfully")
    root.mainloop()


if __name__ == "__main__":
    main()
