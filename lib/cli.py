import inquirer
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from termcolor import colored
import pyfiglet
from sqlalchemy.orm import declarative_base

# Create the database engine and session
DATABASE_URL = 'sqlite:///mydatabase.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

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
def find_or_create_artist(session, title, genre):
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

    with Session() as session:
        find_or_create_artist(session, title, genre)

# Function to find or create a song
def find_or_create_song(session, title, artist_name, release_date, bpm):
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
    with Session() as session:
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

            with Session() as new_artist_session:
                new_artist = find_or_create_artist(new_artist_session, new_artist_name, new_artist_genre)
                artist_name = new_artist.title
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
# not bpm.isdigit() or
        if not bpm:
            bpm = None
        elif not bpm.isdigit() or len(bpm) == 0:
            print(len(bpm) > 0)
            print(colored("Invalid BPM input. BPM set to None.", "red"))
            bpm = None
        else:
            bpm = int(bpm)

        find_or_create_song(session, title, artist_name, release_date, bpm)

# Function to update an artist
def update_artist():
    with Session() as session:
        artist_name = input(colored('Enter Artist Name to update: ',"cyan"))
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

# Function to delete an artist
def delete_artist():
    with Session() as session:
        artist_name = input('Enter Artist Name to delete: ')
        artist = session.query(Artist).filter(Artist.title == artist_name).first()

        if artist:
            session.delete(artist)
            session.commit()
            print(f"Artist Name {artist_name} deleted.")
        else:
            print(colored(f"Artist '{artist_name}' not found.", "red"))

# Function to list artists alphabetically
def list_artists():
    while True:
        with Session() as session:
            artists = session.query(Artist).order_by(Artist.title).all()
            if artists:
                print("List of Artists:")
                artist_choices = [artist.title for artist in artists]
                artist_choices.append("Back")  # Add a "Back" option

                artist_name = inquirer.prompt([
                    inquirer.List('artist_name',
                                  message="Select an artist:",
                                  choices=artist_choices
                                  )
                ])['artist_name']

                if artist_name == "Back":
                    return  # Go back to the previous menu
                else:
                    artist = session.query(Artist).filter(Artist.title == artist_name).first()
                    if artist:
                        print(colored(f"ID: {artist.id}, Name: {artist.title}, Genre: {artist.genre}","cyan"))
                    else:
                        print(colored(f"Artist '{artist_name}' not found.", "red"))
            else:
                print(colored("No artists found in the database.", "red"))

# Function to list songs alphabetically
def list_songs():
    while True:
        with Session() as session:
            songs = session.query(Song).order_by(Song.title).all()
            if songs:
                print("List of Songs:")
                song_choices = [song.title for song in songs]
                song_choices.append(("Back"))  # Add a "Back" option

                song_title = inquirer.prompt([
                    inquirer.List('song_title',
                                  message="Select a song:",
                                  choices=song_choices
                                  )
                ])['song_title']

                if song_title == "Back":
                    return  # Go back to the previous menu
                else:
                    song = session.query(Song).filter(Song.title == song_title).first()
                    if song:
                        artist_name = song.artist.title if song.artist else "Unknown Artist"
                        print(colored(f"ID: {song.id}, Title: {song.title}, Artist: {artist_name}, Release Date: {song.release_date}, BPM: {song.bpm}","cyan"))
                    else:
                        print(colored(f"Song '{song_title}' not found.", "red"))
            else:
                print(colored("No songs found in the database.", "red"))


# Function to manage the main menu
def main():
    while True:
        print(colored("Choose an operation:", "cyan"))
        print(colored("1. Create Artist", "light_yellow"))
        print(colored("2. Create Song", "light_yellow"))
        print(colored("3. Update Artist", "light_yellow"))
        print(colored("4. Delete Artist", "light_yellow"))
        print(colored("5. List Artists", "light_yellow"))
        print(colored("6. List Songs", "light_yellow"))
        print(colored("7. Exit", "light_yellow"))

        choice = input(colored("Enter your choice (1-7): ", "cyan"))

        if choice == '1':
            create_artist()
            ascii_banner = pyfiglet.figlet_format("Great Choice!!")
            print(colored(ascii_banner,"red"))
        elif choice == '2':
            create_song()
            ascii_banner = pyfiglet.figlet_format("Amazing Song!!")
            print(colored(ascii_banner,"red"))
        elif choice == '3':
            update_artist()
            ascii_banner = pyfiglet.figlet_format("BOOM, Artist has been updated!!")
            print(colored(ascii_banner,"red"))
        elif choice == '4':
            delete_artist()
            ascii_banner = pyfiglet.figlet_format("BOOM, Artist has been deleted!!")
            print(colored(ascii_banner,"red"))
        elif choice == '5':
            list_artists()
            ascii_banner = pyfiglet.figlet_format("NOICEEEE!!")
            print(colored(ascii_banner,"red"))
        elif choice == '6':
            list_songs()
            ascii_banner = pyfiglet.figlet_format("VERY NOICEEEEEE!!")
            print(colored(ascii_banner,"red"))
        elif choice == '7':
            ascii_banner = pyfiglet.figlet_format("GoodBye!!")
            print(colored(ascii_banner,"red"))
            break
        else:
            print(colored("Invalid choice. Please enter a valid option (1-7).", "red"))

if __name__ == '__main__':
    main()

