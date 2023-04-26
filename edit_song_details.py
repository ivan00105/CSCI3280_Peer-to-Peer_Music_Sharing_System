import os
from PyQt5 import QtWidgets
from player_window import UI_MainWindow
from pydub import AudioSegment

class EditFile(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI_MainWindow()
        self.ui.buildUiElements(self)

    def edit_audio_details(self, song_selected):
            selected_audio_file = song_selected
            new_title = self.ui.title_edit.text()
            new_artist = self.ui.artist_edit.text()
            new_album = self.ui.album_edit.text()
            print("title:", new_title, ", artist:", new_artist, "album:", new_album)

            if new_title and new_artist and new_album:
                old_file_path = selected_audio_file.path
                extension = os.path.splitext(old_file_path)[1].lower()
                if extension == ".mp3":
                    format = "mp3"
                elif extension in [".wav", ".wave"]:
                    format = "wav"
                else:
                    print("Invalid audio format.")
                    return
                new_file_path = os.path.dirname(old_file_path) + '/' + new_title + extension
                new_lyrics_path = os.path.dirname(old_file_path) + '/' + new_title + '.lrc'
                audio = AudioSegment.from_file(old_file_path, format=format)

                # Update metadata
                audio.export(new_file_path, format=format, tags={
                    'Name': new_title,
                    'Title': new_title,
                    'Contributing artists': new_artist,
                    'Album': new_album
                })
                os.remove(old_file_path)
                print("done")
                selected_audio_file.title = new_title
                selected_audio_file.artist = new_artist
                selected_audio_file.album = new_album
                print("old", os.path.splitext(old_file_path)[0])
                if os.path.exists(os.path.splitext(old_file_path)[0] + '.lrc'):
                    os.rename(os.path.splitext(old_file_path)[0] + '.lrc', new_lyrics_path)

                print(f"Audio file '{selected_audio_file.title}' with Artist '{selected_audio_file.artist}' and Album '{selected_audio_file.album}' has been edited and saved as '{new_title}{extension}'.")
                QtWidgets.QMessageBox.information(None, "Changes Saved", "The changes were successfully saved!")

            else:
                print("Please enter a new title, artist, and album for the audio file.")
