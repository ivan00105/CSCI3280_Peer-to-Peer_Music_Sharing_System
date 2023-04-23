import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import time
import threading

from PIL import Image, ImageTk  # pip install Pillow
from load_local_db import load_local_database

from search import search_music_local, search_music_global
from decoder import AudioPlayer, read_wav_file

class MusicPlayer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Music Player")
        self.geometry("800x600")

        self.is_playing = False
        self.audio_player = None
        self.play_thread = None
        self.current_item = None
        self.setup_widgets()
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.update_progress_bar()  # Call the method to start updating the progress bar
        self.slider_dragging = False  # Add this line to initialize slider_dragging to False
        self.seeking = False


    def toggle_play_pause(self):
        if self.is_playing:
            if self.audio_player:
                self.audio_player.pause()
            self.play_button.configure(image=self.play_image)
        else:
            item = self.treeview.selection()[0] if self.treeview.selection() else None
            if item and not self.audio_player:
                filename = self.treeview.item(item, "values")[0]
                wav_data = read_wav_file("./music/"+filename)
                self.audio_player = AudioPlayer(wav_data, None)
            if self.audio_player:
                self.audio_player.resume()
                self.play_audio()
            self.play_button.configure(image=self.pause_image)
        self.is_playing = not self.is_playing



    def play_audio(self):
        if self.audio_player:
            if not self.play_thread or not self.play_thread.is_alive():
                self.play_thread = threading.Thread(target=self.audio_player.play)
                self.play_thread.start()
            else:
                self.audio_player.resume()

    def on_row_click(self, event, next_song=None):
        selected_items = self.treeview.selection()
        if selected_items:
            item = selected_items[0]
            if item == self.current_item:  # If the user double-clicked the same song
                self.toggle_play_pause()
                return
            self.current_item = item
            print("Playing song:", self.treeview.item(item, "values"))
            if next_song:
                item = next_song
            if self.audio_player:  # If an audio is playing, stop it
                self.audio_player.close()
                self.audio_player = None

            filename = self.treeview.item(item, "values")[0]  # Get the filename from the selected item
            wav_data = read_wav_file("./music/"+filename)  # Read the WAV file
            self.audio_player = AudioPlayer(wav_data, None)  # Create an AudioPlayer instance
            self.play_audio()  # Play the audio

            if not self.is_playing:
                self.is_playing = True
                self.play_button.configure(image=self.pause_image)

    def volume_slider_event(self, value):
        if self.audio_player:
            self.audio_player.set_volume(float(value) / 100)

    def on_seek(self, value):
        if self.audio_player:
            # Calculate the new position in the song
            total_length = len(self.audio_player.wav_data['data'])
            new_position = int((float(value) / 100) * total_length)

            # Calculate audio frame size and adjust new_position
            frame_size = self.audio_player.wav_data['NumChannels'] * self.audio_player.wav_data['BlockAlign']
            new_position = (new_position // frame_size) * frame_size

            # Update the AudioPlayer instance's index
            self.audio_player.set_position(new_position)

    def close_window(self):
        if self.audio_player:
            self.audio_player.close()
        self.destroy()
        
    def previous_song(self):
        if self.current_item:
            prev_item = self.treeview.prev(self.current_item)
            if prev_item:
                self.on_row_click(None, next_song=prev_item)

    def next_song(self):
        if self.current_item:
            next_item = self.treeview.next(self.current_item)
            if next_item:
                self.on_row_click(None, next_song=next_item)

    def update_progress_bar(self):
        if self.audio_player and self.audio_player.playing and not self.slider_dragging:
            total_length = len(self.audio_player.wav_data['data'])
            progress = (self.audio_player.index / total_length) * 100
            self.progress_bar.set(progress)
            print(self.progress_bar.get())
            # Update current time and total time labels
            current_time = self.audio_player.index / self.audio_player.wav_data['ByteRate']
            total_time = total_length / self.audio_player.wav_data['ByteRate']
            self.current_time_label.configure(text="{:d}:{:02d}".format(int(current_time // 60), int(current_time % 60)))
            self.total_time_label.configure(text="{:d}:{:02d}".format(int(total_time // 60), int(total_time % 60)))

        self.after(1000, self.update_progress_bar)  # Call this method every 1000 ms (1 second)

    def on_slider_motion(self, value):
        if self.audio_player:
            self.seeking = True
            self.on_seek(value)
    
    def update_slider(self):
        if not self.seeking:
            self.slider.set(self.current_time)
        self.after(1000, self.update_slider)

    def on_slider_release(self, event):
        if self.audio_player:
            self.seeking = False


    def setup_widgets(self):
        ctk.set_default_color_theme("green")

        # Top frame: Left (Music player) and Right (Lyrics display) panes
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill=tk.BOTH, expand=True)

        # Left pane: Music player
        left_frame = ctk.CTkFrame(top_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        album_art = ctk.CTkLabel(left_frame, text="Album Art")
        album_art.pack(expand=1)

        controls_frame = ctk.CTkFrame(left_frame)
        controls_frame.pack()

        self.progress_bar = ctk.CTkSlider(controls_frame, from_=0, to=100, command=self.on_seek, orientation="horizontal")
        self.progress_bar.set(0,100)
        
        self.progress_bar.bind('<B1-Motion>', lambda event: self.on_slider_motion(self.progress_bar.get()))
        self.progress_bar.bind('<ButtonRelease-1>', self.on_slider_release)
        
        self.current_time_label = ctk.CTkLabel(controls_frame, text="0:00")
        self.current_time_label.pack(side=tk.LEFT)
        self.progress_bar.pack(side=tk.TOP, fill=tk.X)

        self.total_time_label = ctk.CTkLabel(controls_frame, text="0:00")
        self.total_time_label.pack(side=tk.RIGHT)
        
        previous_image = ctk.CTkImage(Image.open("./images/previous.png").resize((25, 25), Image.LANCZOS))
        previous_button = ctk.CTkButton(controls_frame, text='', image=previous_image, width=20, height=20,
                                        command = self.previous_song)
        previous_button.pack(side=tk.LEFT)

        self.play_image = ctk.CTkImage(Image.open("./images/play.png").resize((25, 25), Image.LANCZOS))
        self.pause_image = ctk.CTkImage(Image.open("./images/pause.png").resize((25, 25), Image.LANCZOS))
        self.play_button = ctk.CTkButton(controls_frame, text='', image=self.play_image, width=20, height=20,
                                          command=self.toggle_play_pause)
        self.play_button.pack(side=tk.LEFT)

        next_image = ctk.CTkImage(Image.open("./images/next.png").resize((25, 25), Image.LANCZOS))
        next_button = ctk.CTkButton(controls_frame, text='', image=next_image, width=20, height=20,
                                    command= self.next_song)
        next_button.pack(side=tk.LEFT)

        volume_slider = ctk.CTkSlider(controls_frame, from_=0, to=100, command=self.volume_slider_event)

        volume_slider.pack(side=tk.RIGHT)

        volume_image = ctk.CTkImage(Image.open("./images/volume.png"))
        volume_label = ctk.CTkLabel(controls_frame, text="", image=volume_image)
        volume_label = ctk.CTkLabel(controls_frame, text="", image=volume_image)
        volume_label.pack(side=tk.RIGHT)

        # Right pane: Lyrics display
        right_frame = ctk.CTkFrame(top_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        lyrics_label = ctk.CTkLabel(right_frame, text="Lyrics")
        lyrics_label.pack()

        lyrics_textbox = ctk.CTkTextbox(right_frame, wrap=tk.WORD)
        lyrics_textbox.pack(fill=tk.BOTH, expand=True)

        # Bottom frame: Music list and search
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        search_label = tk.Label(bottom_frame, text="Search")
        search_label.pack()
        search_entry = tk.Entry(bottom_frame)
        search_entry.pack()

        self.treeview = ttk.Treeview(bottom_frame, columns=("File", "Title", "Artist", "Album"), show="headings")
        local_music_db = load_local_database(self.treeview)

        self.treeview.heading("File", text="File")
        self.treeview.heading("Title", text="Title")
        self.treeview.heading("Artist", text="Artist")
        self.treeview.heading("Album", text="Album")
        self.treeview.pack(fill=tk.BOTH, expand=True)

        self.treeview.bind("<Double-1>", lambda event: self.on_row_click(event))
        search_entry.bind("<Return>", lambda event: search_music_local(event, search_entry, self.treeview, local_music_db))



if __name__ == "__main__":
    app = MusicPlayer()
    app.mainloop()
