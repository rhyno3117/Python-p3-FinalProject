import inquirer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Project.OneToMany import Artist, Song

DATABASE_URL = 'sqlite:///mydatabase.db'
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)

def find_or_create_artist(session, title, genre):
    artist = session.query(Artist).filter(Artist.title == title).first()

    if artist is None:
        artist = Artist(title=title, genre=genre)
        session.add(artist)
        session.commit()
        print(f"Artist '{title}' added with ID {artist.id}")
    else:
        print(f"Artist '{title}' already exists with ID {artist.id}")

    return artist

def create_artist():
    title = input('Artist Name: ')
    genre = input('Genre: ')

    with Session() as session:
        find_or_create_artist(session, title, genre)

def find_or_create_song(session, title, artist_id, release_date, bpm):
    song = session.query(Song).filter(Song.title == title).first()

    if song is None:
        song = Song(
            title=title,
            artist_id=artist_id,
            release_date=release_date,
            bpm=bpm
        )
        session.add(song)
        session.commit()
        print(f"Song '{title}' added with ID {song.id}")
    else:
        print(f"Song '{title}' already exists with ID {song.id}")

    return song

def create_song():
    with Session() as session:
        artists = session.query(Artist).all()
        artist_choices = {str(artist.id): artist.title for artist in artists}

        title = input('Song Title: ')
        artist_id = input('Select Artist (ID): ')
        release_date = input('Release Date: ')
        bpm = input('BPM (optional): ')

        if not title:
            print("Song Title cannot be empty.")
            return

        if artist_id not in artist_choices:
            print("Invalid Artist ID.")
            return

        if not release_date:
            print("Release Date cannot be empty.")
            return

        if not bpm:
            bpm = None
        elif not bpm.isdigit() or len(bpm) != 3:
            print("Invalid BPM input. BPM set to None.")
            bpm = None
        else:
            bpm = int(bpm)

        find_or_create_song(session, title, int(artist_id), release_date, bpm)

def update_artist():
    with Session() as session:
        artist_id = input('Enter Artist ID to update: ')
        artist = session.query(Artist).filter(Artist.id == int(artist_id)).first()

        if artist:
            new_title = input('New Artist Name: ')
            new_genre = input('New Genre: ')
            artist.title = new_title
            artist.genre = new_genre
            session.commit()
            print(f"Artist ID {artist.id} updated.")
        else:
            print(f"Artist ID {artist_id} not found.")

def delete_artist():
    with Session() as session:
        artist_id = input('Enter Artist ID to delete: ')
        artist = session.query(Artist).filter(Artist.id == int(artist_id)).first()

        if artist:
            session.delete(artist)
            session.commit()
            print(f"Artist ID {artist.id} deleted.")
        else:
            print(f"Artist ID {artist_id} not found.")

def list_artists():
    with Session() as session:
        artists = session.query(Artist).all()
        if artists:
            print("List of Artists:")
            for artist in artists:
                print(f"ID: {artist.id}, Name: {artist.title}, Genre: {artist.genre}")
        else:
            print("No artists found in the database.")

def list_songs():
    with Session() as session:
        songs = session.query(Song).all()
        if songs:
            print("List of Songs:")
            for song in songs:
                artist_name = song.artist.title if song.artist else "Unknown Artist"
                print(f"ID: {song.id}, Title: {song.title}, Artist: {artist_name}, Release Date: {song.release_date}, BPM: {song.bpm}")
        else:
            print("No songs found in the database.")

def main():
    while True:
        print("Choose an operation:")
        print("1. Create Artist")
        print("2. Create Song")
        print("3. Update Artist")
        print("4. Delete Artist")
        print("5. List Artists")
        print("6. List Songs")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            create_artist()
        elif choice == '2':
            create_song()
        elif choice == '3':
            update_artist()
        elif choice == '4':
            delete_artist()
        elif choice == '5':
            list_artists()
        elif choice == '6':
            list_songs()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please enter a valid option (1-7).")

if __name__ == '__main__':
    main()
