import inquirer
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from termcolor import colored
import pyfiglet
from sqlalchemy.orm import declarative_base
from termcolor import colored
import pyfiglet


# Create the database engine and session
DATABASE_URL = 'sqlite:///mydatabase.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()  # Create a session instance

# Create the base class for declarative models
Base = declarative_base()

# Define the Artist and Song classes
class Artist(Base):
    __tablename__ = 'artist_table'
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, nullable=False)
    genre = Column(String)
    songs = relationship('Song', backref='artist')

class Song(Base):
    __tablename__ = 'songs_table'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Text)
    bpm = Column(Integer)
    artist_id = Column(Integer, ForeignKey('artist_table.id'))

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Function to find or create an artist
def find_or_create_artist(title, genre):
    artist = session.query(Artist).filter(Artist.title == title).first()

    if artist is None:
        artist = Artist(title=title, genre=genre)
        session.add(artist)
        session.commit()
        print(colored(f"Artist '{title}' added with ID {artist.id}", "green"))
    else:
        print(colored(f"Artist '{title}' already exists with ID {artist.id}", "red"))

    return artist

# Function to create an artist
def create_artist():
    title = input(colored('Artist Name: ', "light_yellow"))
    genre = input(colored('Genre: ', "light_yellow"))

    find_or_create_artist(title, genre)

# Function to find or create a song
def find_or_create_song(title, artist_name, release_date, bpm):
    artist = session.query(Artist).filter(Artist.title == artist_name).first()

    if artist is None:
        print(colored(f"Artist '{artist_name}' not found. Song not created.", "red"))
        return

    song = session.query(Song).filter(Song.title == title, Song.artist_id == artist.id).first()

    if song is None:
        song = Song(
            title=title,
            artist_id=artist.id,
            release_date=release_date,
            bpm=bpm
        )
        session.add(song)
        session.commit()
        print(colored(f"Song '{title}' added with ID {song.id}", "green"))
    else:
        print(colored(f"Song '{title}' already exists with ID {song.id}", "red"))

# Function to create a song
def create_song():
    artists = session.query(Artist).all()
    artist_choices = {artist.title: artist for artist in artists}

    title = input(colored('Song Title: ', "light_yellow"))
    artist_name = input(colored('Select Artist or enter "new" to create a new artist: ', "light_yellow"))

    if artist_name.lower() == "new":
        # Create a new artist
        new_artist_name = input(colored('New Artist Name: ', "light_yellow"))
        new_artist_genre = input(colored('Genre: ', "light_yellow"))

        if not new_artist_name:
            print(colored("Artist Name cannot be empty.", "red"))
            return

        find_or_create_artist(new_artist_name, new_artist_genre)
        artist_name = new_artist_name
    elif artist_name not in artist_choices:
        print(colored("Invalid Artist Name.", "red"))
        return

    release_date = input(colored('Release Date: ', "light_yellow"))
    bpm = input(colored('BPM (optional): ', "light_yellow"))

    if not title:
        print(colored("Song Title cannot be empty.", "red"))
        return

    if not release_date:
        print(colored("Release Date cannot be empty.", "red"))
        return

    if not bpm:
        bpm = None
    elif not bpm.isdigit() or len(bpm) == 0:
        print(colored("Invalid BPM input. BPM set to None.", "red"))
        bpm = None
    else:
        bpm = int(bpm)

    find_or_create_song(title, artist_name, release_date, bpm)

# Function to update an artist
def update_artist():
    artist_name = input(colored('Enter Artist Name to update:', "cyan"))
    artist = session.query(Artist).filter(Artist.title == artist_name).first()

    if artist:
        new_title = input('New Artist Name: ')
        new_genre = input('New Genre: ')
        artist.title = new_title
        artist.genre = new_genre
        session.commit()
        print(colored(f"Artist Name {artist_name} updated.", "green"))
    else:
        print(colored(f"Artist '{artist_name}' not found.", "red"))

# Function to delete an artist by name or ID
def delete_artist():
    artist_input = input('Enter Artist Name or ID to delete: ')
    
    if artist_input.isdigit():
        artist = session.query(Artist).filter(Artist.id == int(artist_input)).first()
    else:
        artist = session.query(Artist).filter(Artist.title == artist_input).first()

    if artist:
        session.delete(artist)
        session.commit()
        print(f"Artist {artist.title} (ID: {artist.id}) deleted.")
    else:
        print(colored(f"Artist '{artist_input}' not found.", "red"))

# Function to delete a song by title or ID
def delete_song():
    song_input = input('Enter Song Title or ID to delete: ')

    # Check if the input is a digit (ID) or not (Title)
    if song_input.isdigit():
        song = session.query(Song).filter(Song.id == int(song_input)).first()
    else:
        song = session.query(Song).filter(Song.title == song_input).first()

    if song:
        session.delete(song)
        session.commit()
        print(f"Song '{song.title}' (ID: {song.id}) deleted.")
    else:
        print(colored(f"Song '{song_input}' not found.", "red"))

# Function to list songs by a selected artist
def list_songs_by_artist(artist):
    songs = session.query(Song).filter(Song.artist_id == artist.id).all()
    if songs:
        print(colored(f"Songs by {artist.title}:", "cyan"))
        for song in songs:
            print(
                colored(f"{colored('ID:', 'yellow')} {colored(song.id, 'green')}, "
                        f"{colored('Title:', 'yellow')} {colored(song.title, 'green')}, "
                        f"{colored('Release Date:', 'yellow')} {colored(song.release_date, 'green')}, "
                        f"{colored('BPM:', 'yellow')} {colored(song.bpm, 'green')}",
                        "cyan")
            )
    else:
        print(colored(f"No songs found for {artist.title}.", "red"))

# Function to list artists
def list_artists():
    while True:
        artists = session.query(Artist).order_by(Artist.title).all()
        if artists:
            # Print a bigger "List of Artists" text
            ascii_banner = pyfiglet.figlet_format("Artists", font="big")
            print(colored(ascii_banner, "red"))

            artist_choices = [artist.title for artist in artists]
            artist_choices.append("Back")  # Add a "Back" option
            # Remove the "Delete Artist by ID" option
            artist_name = inquirer.prompt([
                inquirer.List('artist_name',
                              message=colored("Select an artist:", "cyan"),
                              choices=artist_choices
                              )
            ])['artist_name']

            if artist_name == "Back":
                return  # Go back to the previous menu
            else:
                artist = session.query(Artist).filter(Artist.title == artist_name).first()
                if artist:
                    # Display artist.id, artist.title, and artist.genre in green, and "Id:", "Name:", "Genre:" in cyan
                    print(
                        f"{colored('Id:', 'yellow')} {colored(artist.id, 'green')}, "
                        f"{colored('Name:', 'yellow')} {colored(artist.title, 'green')}, "
                        f"{colored('Genre:', 'yellow')} {colored(artist.genre, 'green')}"
                    )

                    # Option to list songs for the selected artist
                    list_songs_option = input(colored("List songs for this artist? (y/n): ", "cyan"))
                    if list_songs_option.lower() == "y":
                        list_songs_by_artist(artist)
                else:
                    print(colored(f"Artist '{artist_name}' not found.", "red"))
        else:
            print(colored("No artists found in the database.", "red"))


# Function to list songs alphabetically
def list_songs():
    while True:
        songs = session.query(Song).order_by(Song.title).all()
        if songs:
            ascii_banner = pyfiglet.figlet_format("Songs", font="big")
            print(colored(ascii_banner, "red"))
            song_choices = [song.title for song in songs]
            song_choices.append("Back")  # Add a "Back" option
            # Remove the "Delete Song by ID" option
            song_title = inquirer.prompt([
                inquirer.List('song_title',
                              message=colored("Select a song:", "cyan"),
                              choices=song_choices
                              )
            ])['song_title']

            if song_title == "Back":
                return  # Go back to the previous menu
            else:
                song = session.query(Song).filter(Song.title == song_title).first()
                if song:
                    artist_name = song.artist.title if song.artist else "Unknown Artist"
                    print(
                        colored(f"{colored('ID:', 'yellow')} {colored(song.id, 'green')}, "
                                f"{colored('Title:', 'yellow')} {colored(song.title, 'green')}, "
                                f"{colored('Artist:', 'yellow')} {colored(artist_name, 'green')}, "
                                f"{colored('Release Date:', 'yellow')} {colored(song.release_date, 'green')}, "
                                f"{colored('BPM:', 'yellow')} {colored(song.bpm, 'green')}",
                                "cyan")
                    )
                else:
                    print(colored(f"Song '{song_title}' not found.", "red"))
        else:
            print(colored("No songs found in the database.", "red"))


# Function to list songs by BPM
def list_songs_by_bpm():
    songs = session.query(Song).order_by(Song.bpm).all()
    if songs:
        print(colored("List of Songs by BPM:","cyan"))
        for song in songs:
            artist_name = song.artist.title if song.artist else "Unknown Artist"
            bpm = song.bpm if song.bpm is not None else "N/A"
            
            # Colorize labels and values separately with the desired order
            formatted_output = (
                f"{colored('BPM:', 'yellow')} {colored(bpm, 'green')}, "
                f"{colored('Title:', 'yellow')} {colored(song.title,'green')}, "
                f"{colored('Artist:', 'yellow')} {colored(artist_name,'green')}, "
                f"{colored('Release Date:', 'yellow')} {colored(song.release_date,'green')}, "
                f"{colored('ID:', 'yellow')} {colored(song.id,'green')}"
            )
            
            print(formatted_output)
    else:
        print(colored("No songs found in the database.", "red"))
# Function to manage the main menu
# ... (previous code)

# Function to manage the main menu
def main():
    while True:
        ascii_banner = pyfiglet.figlet_format("RYME")
        print(colored(ascii_banner, "cyan"))
        print(colored("Choose an operation:", "cyan"))
        print(colored("1. Add Artist", "light_yellow"))
        print(colored("2. Add Song", "light_yellow"))
        print(colored("3. Update Artist", "light_yellow"))
        print(colored("4. Delete Artist", "light_yellow")) 
        print(colored("5. Delete Song", "light_yellow"))  # Add the option to delete a song
        print(colored("6. Lists", "light_yellow"))  # Create a submenu for listing operations
        print(colored("7. Exit", "light_yellow"))  # Update the exit option

        choice = input(colored("Enter your choice (1-7): ", "cyan"))

        if choice == '1':
            create_artist()
            ascii_banner = pyfiglet.figlet_format("Artist is Added!!")
            print(colored(ascii_banner, "red"))
        elif choice == '2':
            create_song()
            ascii_banner = pyfiglet.figlet_format("Song is Added!!")
            print(colored(ascii_banner, "red"))
        elif choice == '3':
            update_artist()
        elif choice == '4':
            delete_artist()
        elif choice == '5':
            delete_song()  
        elif choice == '6':
            list_operations()  # Call the new function for listing operations
        elif choice == '7':  
            ascii_banner = pyfiglet.figlet_format("GoodBye!!")
            print(colored(ascii_banner, "red"))
            break
        else:
            print(colored("Invalid choice. Please enter a valid option (1-7).", "red"))

# Function to manage the list operations submenu
def list_operations():
    while True:
        print(colored("List Operations:", "cyan"))
        print(colored("1. Artists", "light_yellow"))
        print(colored("2. Songs", "light_yellow"))
        print(colored("3. BPM", "light_yellow"))
        print(colored("4. Back to Main Menu", "light_yellow"))

        choice = input(colored("Enter your choice (1-4): ", "cyan"))

        if choice == '1':
            # ascii_banner = pyfiglet.figlet_format("Artists!!")
            # print(colored(ascii_banner, "red"))
            list_artists()
        elif choice == '2':
            # ascii_banner = pyfiglet.figlet_format("Songs!!")
            # print(colored(ascii_banner, "red"))
            list_songs()
        elif choice == '3':
            ascii_banner = pyfiglet.figlet_format("BPM!!")
            print(colored(ascii_banner, "red"))
            list_songs_by_bpm()
        elif choice == '4':
            break
        else:
            print(colored("Invalid choice. Please enter a valid option (1-4).", "red"))

if __name__ == '__main__':
    main()
