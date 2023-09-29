# RYME - Music Database

## Introduction

RYME is a Python command-line application for managing a music database. It allows you to add, update, and delete artists and songs. You can also list artists, songs, and songs sorted by BPM. Here's a breakdown of its features and how to use it.

# Table of Contents
1. Setup
2. Usage
3. Functions
4. Main Menu
5. List Operations
6. Contributing
7. License

# Setup
Before you can use RYME, make sure you have the required Python libraries installed. You can install them using pip

Once you have the dependencies installed, you're ready to set up the database. RYME uses an SQLite database by default, which will be created in the same directory as the script.

# Usage
You can interact with RYME through a command-line interface.

# Functions
RYME provides the following functions:

a. Add Artist
Allows you to add a new artist to the database.
You need to provide the artist's name and genre.
If the artist already exists, it will update the genre.

b. Add Song
Lets you add a new song to the database.
You can provide the song's title, artist (existing or new), release date, and BPM (optional).
You can create a new artist while adding a song.

c. Update Artist
Allows you to update an artist's name or genre.
Enter the artist's name to update, and then provide the new name and/or genre.

d. Delete Artist
Lets you delete an artist by their name or ID.
Enter the artist's name or ID to delete.
e. Delete Song

Allows you to delete a song by its title or ID.
Enter the song's title or ID to delete.
f. Lists

Provides a submenu for listing operations:
List Artists: Displays a list of all artists in the database.
List Songs: Displays a list of all songs in the database.
List Songs by BPM: Displays songs sorted by BPM.
Back to Main Menu: Returns to the main menu.

# Main Menu
The main menu provides options to access the various functions of RYME. To use the main menu:

Run the script: python your_script_name.py
Choose an operation by entering a number from 1 to 7:
1: Add Artist
2: Add Song
3: Update Artist
4: Delete Artist
5: Delete Song
6: Lists (for listing operations)
7: Exit

# List Operations
The "Lists" submenu allows you to list artists, songs, and songs sorted by BPM. To use the list operations:

Choose the "6: Lists" option from the main menu.
Choose an operation by entering a number from 1 to 4:
1: List Artists
2: List Songs
3: List Songs by BPM
4: Back to Main Menu

# Contributing
Contributions to RYME are welcome! If you have any ideas for improvements or find any issues, please open an issue or create a pull request on the RYME GitHub repository.

# License
RYME is released under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license.
