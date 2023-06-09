import shutil
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt, QUrl, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QFontDatabase, QIcon
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QLabel, QLineEdit, QVBoxLayout, QLabel, QLineEdit, QListWidget
from PyQt5.QtGui import QColor
import os
import random
import json
from audio_visualizer import AudioVisualizer
from database import SqliteDB
from player_window import UI_MainWindow
from decode import Song
from edit_song_details import EditFile
from peer import Peer
from PyQt5.QtCore import QThread, pyqtSignal, QThread
from PyQt5.QtCore import QBuffer, QIODevice, QObject
from PyQt5.QtCore import QIODevice, QByteArray, QDataStream, QBuffer



import threading
import time
import socket
import pyaudio
from queue import Queue


class SaveSongWorker(QObject):
    finished = pyqtSignal()

    def __init__(self, save_function, song_data, song_name):
        super().__init__()
        self.save_function = save_function
        self.song_data = song_data
        self.song_name = song_name

    def run(self):
        self.save_function(self.song_data, self.song_name)
        self.finished.emit()

class StreamingBuffer(QIODevice):
    def __init__(self, total_data_size, parent=None):
        super(StreamingBuffer, self).__init__(parent)
        self.total_data_size = total_data_size
        self.data = QByteArray()
        self.buffer = QBuffer(self.data, self)
        self.open(QIODevice.ReadOnly)

    def writeData(self, data):
        self.buffer.open(QIODevice.Append)
        written = self.buffer.write(data)
        self.buffer.close()
        # Check if the buffer has reached 50% of the total data size
        if self.buffer.size() > self.total_data_size * 0.5:
            self.buffer.seek(0)
            self.readyRead.emit()
        return written
    def readData(self, maxlen):
        return self.buffer.read(maxlen)

    def isSequential(self):
        return True

class MusicPlayer(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI_MainWindow()
        self.ui.buildUiElements(self)
        self.setWindowFlags(
            Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)
        self.setStyleSheet("background-color:transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        self.ui.centralwidget.setMouseTracking(True)
        self.ui.widget.setMouseTracking(True)
        self.ui.widget_bottom.setMouseTracking(True)
        self.move_drag = False
        self.move_DragPosition = 0
        self.right_bottom_corner_drag = False
        self.left_bottom_corner_drag = False
        self.left_drag = False
        self.right_drag = False
        self.bottom_drag = False
        self.left_rect = []
        self.right_rect = []
        self.bottom_rect = []
        self.right_bottom_corner_rect = []
        self.left_bottom_corner_rect = []

        # bind buttons
        self.ui.btn_play.clicked.connect(self.song_start_switch)
        self.ui.pushButton_path.clicked.connect(self.fetch_songs_from_directory)
        self.ui.pushButton_song_find.clicked.connect(self.song_find)
        self.ui.playlist_listWidget.doubleClicked.connect(self.song_double_clicked)
        self.ui.lyric_listWidget.doubleClicked.connect(self.lyrics_double_clicked)
        self.ui.AudioInfo_listWidget.doubleClicked.connect(self.info_double_clicked)
        self.ui.search_field.textChanged.connect(self.search_song)
        self.ui.btn_next.clicked.connect(self.play_next)
        self.ui.button_prev.clicked.connect(self.play_last)
        self.ui.hSlider.sliderReleased.connect(self.slider_release)
        self.ui.hSlider.sliderPressed.connect(self.slider_press)
        self.ui.hSlider.sliderMoved.connect(self.slider_move)

        self.lyric_timer = QTimer(self)
        self.lyric_timer.timeout.connect(self.song_timer)

        self.media_player = QMediaPlayer(flags=QMediaPlayer.Flags())
        self.song_path_playlist = []
        self.local_path_list = []
        self.local_songs_count = 0
        self.directory_path = ''
        self.song_current_path = ''
        self.is_window_maximized = False
        self.volume_change_mode = 0
        self.sort_mode = 0
        self.is_started = False
        self.is_sliderPress = False
        self.lyric_time_index = 0
        self.song_index = 0
        self.song_selected = Song(None)
        self.song_path_list = []
        self.lyric_time_list = []
        self.play_mode = 0
        self.lyric_mode = 0

        self.ui.search_field.setClearButtonEnabled(True)
        self.media_player.setVolume(90)

        self.ui.lyric_listWidget.setWordWrap(True)
        self.ui.AudioInfo_listWidget.setWordWrap(True)
        self.ui.label_name.setWordWrap(True)

        self.ui.playlist_listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.playlist_listWidget.verticalScrollBar().setSingleStep(15)
        self.ui.lyric_listWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.lyric_listWidget.verticalScrollBar().setSingleStep(15)

        self.thread_load_songs = DBThread()
        self.thread_load_songs.item_signal.connect(self.thread_search_num)
        self.thread_load_songs.stop_signal.connect(self.thread_search_stop)

        """network"""
        self.peer = Peer(12345, "172.20.10.7", 50000, self)
        self.peer.song_list_received.connect(self.update_received_song_list)
        self.register_thread = threading.Thread(target=self.peer.register_with_tracker)
        self.register_thread.daemon = True
        self.register_thread.start()
        self.server_thread = threading.Thread(target=self.peer.start_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        # self.update_thread = UpdatePeersThread(self)
        # self.update_thread.start()
        self.received_song_list = []
        self.all_received_song_list = []
        self.local_song_list = []
        self.client_thread = threading.Thread(target=self.peer.start_client, name="client_thread")
        self.client_thread.daemon = True
        self.client_thread.start()
        self.current_search_text = ""

        self.db_path = SqliteDB.db_path
        self.setting_path = 'config.json'

        if os.path.exists(self.db_path):
            self.load_config()

    def load_config(self):
        if not os.path.exists(self.setting_path):
            return
        with open('config.json') as f:
            config = json.load(f)
            self.directory_path = config.get('directory_path')
            if self.directory_path:
                self.update_songs_list()

            self.lyric_mode = config.get('lrc_mode', 0)

            self.sort_mode = config.get('sort_mode', 0)
            self.set_sort_mode_stylesheet()

            if os.path.exists(self.db_path):
                self.select_songs('')
                self.song_path_playlist = self.song_path_list.copy()

            self.play_mode = config.get('play_mode', 0)
            self.set_play_mode()
            self.set_play_mode_stylesheet()

    def save_config(self):
        config = {
            "directory_path": self.directory_path,
            "play_mode": self.play_mode,
            "lrc_mode": self.lyric_mode,
            "player_volume": self.media_player.volume(),
            "sort_mode": self.sort_mode
        }
        with open(self.setting_path, 'w') as f:
            json.dump(config, f)

    def slider_move(self):
        self.ui.label_time_start.setText(self.ms_to_str(self.ui.hSlider.value()))

    def slider_release(self):
        self.media_player.setPosition(self.ui.hSlider.value())
        self.lyric_time_index = 0
        self.is_sliderPress = False

    def slider_press(self):
        self.is_sliderPress = True

    def lyrics_double_clicked(self):
        if len(self.lyric_time_list) != 0:
            self.is_started = True
            print(f'Jump to{self.lyric_time_list[self.ui.lyric_listWidget.currentRow()]}')
            self.media_player.setPosition(self.lyric_time_list[self.ui.lyric_listWidget.currentRow()])
            self.lyric_time_index = 0

    @staticmethod
    def ms_to_str(ms):
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        return f'{str(m).zfill(2)}:{str(s).zfill(2)}'

    def song_timer(self):
        if not self.is_sliderPress:
            self.ui.label_time_start.setText(self.ms_to_str(self.media_player.position()))
            self.ui.label_time_end.setText(self.ms_to_str(self.media_player.duration()))
        if len(self.lyric_time_list) != 0:
            while True:
                if self.lyric_time_index > len(self.lyric_time_list) - 1:
                    break
                elif self.lyric_time_list[self.lyric_time_index] < self.media_player.position():
                    self.lyric_time_index += 1
                else:
                    break
            self.ui.lyric_listWidget.setCurrentRow(self.lyric_time_index - 1)
            item = self.ui.lyric_listWidget.item(self.lyric_time_index - 1)
            self.ui.lyric_listWidget.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtCenter)

        self.ui.hSlider.setMaximum(self.media_player.duration())
        self.ui.hSlider.setMinimum(0)

        if not self.is_sliderPress:
            self.ui.hSlider.setValue(self.media_player.position())

        if self.media_player.position() == self.media_player.duration():
            print('Time over')
            self.play_next()


    def set_sort_mode_stylesheet(self):
        if self.sort_mode == 0:
            text = 'Sort by alphabetical order'
        elif self.sort_mode == 1:
            text = 'Sort by modification time'
        else:
            text = 'Sort by creation time'

    def set_play_mode(self):
        if self.play_mode == 0:
            self.song_path_playlist.sort(key=lambda x: x['index'])
            if self.song_current_path != '':
                for item in self.song_path_playlist:
                    if item['path'] == self.song_current_path:
                        self.song_index = self.song_path_playlist.index(item)
        elif self.play_mode == 1:
            pass
        elif self.play_mode == 2:
            random.shuffle(self.song_path_playlist)

    def set_play_mode_stylesheet(self):
        return

    def close_window(self):
        self.save_config()
        QCoreApplication.quit()

    def maximize_window(self):
        if self.is_window_maximized:
            self.showNormal()
            self.is_window_maximized = False
        else:
            self.showMaximized()
            self.is_window_maximized = True

    def fetch_songs_from_directory(self):
        # self.song_pause()
        self.directory_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'choose directory', '',
                                                                         options=QtWidgets.QFileDialog.ShowDirsOnly)
        if not self.directory_path:
            return
        self.song_index = 0
        self.ui.playlist_listWidget.clear()
        self.songs_count()
        if self.local_songs_count == 0:
            mess_str = 'no proper music file'
            print(mess_str)
            QtWidgets.QMessageBox.information(self, "cannot find music file", mess_str, QtWidgets.QMessageBox.Ok)
        else:
            self.ui.hSlider.setMaximum(self.local_songs_count)
            self.ui.hSlider.setMinimum(0)
            self.thread_load_songs.directory_path = self.directory_path
            self.thread_load_songs.start()

    def songs_count(self):
        path_list = []
        for root, dirs, items in os.walk(self.directory_path):
            for item in items:
                file_path = f'{root}/{item}'
                suffix = file_path.split('.')[-1].lower()
                suffix_limit = ['wav', 'wave', 'mp3']
                if suffix not in suffix_limit:
                    continue
                path_list.append(file_path)
        self.local_songs_count = len(path_list)
        self.local_path_list = path_list

    def thread_search_num(self, data):
        self.ui.hSlider.setValue(data)

    def thread_search_stop(self):
        self.select_songs('')
        self.song_path_playlist = self.song_path_list.copy()
        self.set_play_mode()
        self.save_config()

    def search_song(self):
        if os.path.exists(self.db_path):
            self.select_songs(self.ui.search_field.text())

    def select_songs(self, text):
        cloud_item_lst = []
        for received_item in self.all_received_song_list:
            if text in received_item:
                cloud_item_lst.append(received_item)

        with SqliteDB() as us:
            text = '%{}%'.format(text)
            sql = """
            select * from music_info 
            where title like ? or artist like ? or album like ? or genre like ? or date like ? or file_name like ?
            """
            params = (text, text, text, text, text, text)
            result = us.fetch_all(sql, params)

        for item in result:
            if item['title'] == 'None':
                item['title'] = item['file_name']

        self.ui.playlist_listWidget.clear()
        self.song_path_list = []
        count = 0
        for item in result:
            icon_path = "images/local.png"
            icon = QIcon(icon_path)
            item_text = f"{item['title']}\n- {item['artist']}"
            item_w = QListWidgetItem()
            item_w.setText(item_text)
            item_w.setIcon(icon)
            self.ui.playlist_listWidget.addItem(item_w)

            self.song_path_list.append({
                'index': count,
                'path': item['path'],
                'is_local': True
            })
            count += 1

        for item in cloud_item_lst:
            icon_path = "images/cloud.png"
            icon = QIcon(icon_path)
            item_text = item
            item_w = QListWidgetItem()
            item_w.setText(item_text)
            item_w.setIcon(icon)
            self.ui.playlist_listWidget.addItem(item_w)
            self.song_path_list.append({
                'index': count,
                'path': item,
                'is_local': False
            })
            count += 1

        self.local_songs_count = count



    def update_songs_list(self):

        def list_compare(local_list, db_list):
            local_list = set(local_list)
            db_list = set(db_list)
            _updated_list = local_list - db_list
            _removed_list = db_list - local_list
            return _updated_list, _removed_list

        self.songs_count()

        with SqliteDB() as us:
            sql = 'select path from music_info'
            results = us.fetch_all(sql)
            db_paths = [result['path'] for result in results]

            updated_paths, removed_paths = list_compare(self.local_path_list, db_paths)

            if len(updated_paths) == 0 and len(removed_paths) == 0:
                print('counted fine')
            else:
                for path in updated_paths:
                    self.insert_song_into_db(path, us)
                    print(f'inserted{path}')

                for path in removed_paths:
                    self.delete_song_from_db(path, us)
                    print(f'removed{path}')

                QtWidgets.QMessageBox.information(self, "datebase updated", QtWidgets.QMessageBox.Ok)

    def insert_song_into_db(self, path, us):
        song = Song(path)
        sql = """
            insert into music_info (file_name, path, title, artist, album, date, genre, mtime, ctime) 
            values (?,?,?,?,?,?,?,?,?)
        """
        file_name = song.path.split('/')[-1]
        get_mtime = int(os.path.getmtime(song.path))
        get_ctime = int(os.path.getctime(song.path))
        params = (file_name, song.path, song.title, song.artist, song.album, song.date, song.genre, get_mtime, get_ctime)
        us.cursor.execute(sql, params)

    def delete_song_from_db(self, path, us):
        sql = """
            delete from music_info
            where path like ?
        """
        params = (path,)
        us.cursor.execute(sql, params)


    def song_start_switch(self):
        if self.song_current_path == '' and self.local_songs_count != 0:
            self.play_next()
            return
        elif self.song_current_path == '':
            return
        print("calling song start")


        self.volume_buffer = self.media_player.volume()
        self.volume_add_buffer = 0
        if self.is_started is True:
            self.audio_visualizer.stop_animation()
            self.pause_music()
        else:
            self.audio_visualizer.resume_animation()
            self.volume_smooth_low_mode = False
            self.play_music()

    def song_find(self):
        flag = False
        song_index = 0
        for item in self.song_path_list:
            if item['path'] == self.song_current_path:
                # item.setForeground(QColor("#FFFFFF"))
                song_index = self.song_path_list.index(item)
                flag = True
        if flag:
            self.ui.playlist_listWidget.setCurrentRow(song_index)
            item = self.ui.playlist_listWidget.item(song_index)
            item.setForeground(QColor("#FFFFFF"))
            self.ui.playlist_listWidget.scrollToItem(item, QtWidgets.QAbstractItemView.PositionAtTop)

    def save_playlist(self):
        self.song_path_playlist = self.song_path_list.copy()
        self.set_play_mode()
        QtWidgets.QMessageBox.information(self, "save successfully", 'the playlist has been replaced',
                                          QtWidgets.QMessageBox.Ok)

    def song_double_clicked(self):
        song_index = self.ui.playlist_listWidget.currentRow()
        song_dict: dict = self.song_path_list[song_index]
        self.song_current_path = song_dict['path']
        is_local = song_dict['is_local']

        if is_local:
            # # Handle local song playback
            # if self.play_mode == 2:  # random
            #     random.shuffle(self.song_path_playlist)

            for item in self.song_path_playlist:
                if item['path'] == self.song_current_path:
                    self.song_index = self.song_path_playlist.index(item)
            self.play_init()
        else:
            #TODO
            self.peer.request_song(song_dict['path'])

    def save_song_to_file(self, song_data, song_name):
        song_path = os.path.join(self.directory_path, song_name)
        with open(song_path, 'wb') as file:
            file.write(song_data)
    
    def on_save_song_finished(self):
        print("Song saved successfully")

    def play_received_song_pyaudio(self, song_data, song_name):
        # Save the received song data to a file
        self.save_song_to_file(song_data, song_name)

        # Initialize a PyAudio stream
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=2,
            rate=44100,
            output=True,
            frames_per_buffer=1024,
        )

        # Create a QBuffer to store the received song data
        self.buffer = QBuffer()
        self.buffer.open(QIODevice.ReadWrite)
        self.buffer.write(song_data)

        # Seek to the beginning of the buffer
        self.buffer.seek(0)

        # Calculate the buffer size for 50% of the song
        buffer_size = int(len(song_data) * 0.5)

        # Create a queue to store the audio chunks
        audio_queue = Queue()

        # Function to read the audio chunks and put them in the queue
        def read_audio():
            while True:
                data = self.buffer.read(buffer_size)
                if not data:
                    break
                audio_queue.put(data)

        # Function to play the audio chunks from the queue
        def play_audio():
            # Wait until enough data is buffered
            while audio_queue.qsize() < 5:
                time.sleep(0.1)

            while True:
                data = audio_queue.get()
                if not data:
                    break
                stream.write(data)

            # Stop the stream and close PyAudio
            stream.stop_stream()
            stream.close()
            p.terminate()

        # Start reading the audio chunks in a new thread
        read_thread = threading.Thread(target=read_audio)
        read_thread.start()

        # Start playing the audio chunks in a new thread
        play_thread = threading.Thread(target=play_audio)
        play_thread.start()



    def play_received_song(self, song_data, song_name):
        # Create a SaveSongWorker instance
        save_worker = SaveSongWorker(self.save_song_to_file, song_data, song_name)

        # Create a new QThread for the worker
        save_thread = QThread(self)
        save_worker.moveToThread(save_thread)
        # Connect signals and slots
        save_thread.started.connect(save_worker.run)
        save_worker.finished.connect(save_thread.quit)
        save_worker.finished.connect(save_worker.deleteLater)
        save_thread.finished.connect(save_thread.deleteLater)
        # Start the thread
        save_thread.start()

        # Create a StreamingBuffer instance
        total_data_size = len(song_data)
        self.buffer = StreamingBuffer(total_data_size)
        self.buffer.write(song_data)

        # Set the media player to use the buffer as the source
        self.media_player.setMedia(QMediaContent(None), self.buffer)

        # Play the song
        self.play_init()




    def info_double_clicked(self):
        if self.song_current_path:
            text = self.ui.AudioInfo_listWidget.currentItem().text().split('：')[-1]
            self.ui.search_field.setText(text)

    def play_init(self):
        self.media_player.setMedia(QMediaContent(QUrl(self.song_current_path)))
        self.initialize_song_data()
        self.play_music()

    def play_next(self):
        print('Next')
        print(self.song_path_playlist)
        if len(self.song_path_playlist) == 0:
            return
        elif self.play_mode != 1 and self.song_current_path != '':
            self.song_index += 1
            if self.song_index > len(self.song_path_playlist) - 1:
                self.song_index = 0
        self.song_current_path = self.song_path_playlist[self.song_index]['path']
        self.play_init()
        self.song_find()

    def play_last(self):
        print('Last')
        if len(self.song_path_playlist) == 0:
            return
        elif self.play_mode != 1 and self.song_current_path != '':
            self.song_index -= 1
            if self.song_index < 0 or (self.song_index > len(self.song_path_playlist) - 1):
                self.song_index = len(self.song_path_playlist) - 1
        self.song_current_path = self.song_path_playlist[self.song_index]['path']
        self.play_init()
        self.song_find()

    def play_music(self):
        self.media_player.play()
        self.lyric_timer.start(500)
        self.is_started = True
        print('Play')
        self.ui.btn_play.setToolTip('Pause')
        self.ui.btn_play.setStyleSheet("image: url(images/pause.png);")
        # AudioVisualizer.resume_animation(self)

    def pause_music(self):
        # a = AudioVisualizer(self.song_selected.path)
        # AudioVisualizer.stop_animation(a,"sooraj")
        self.media_player.pause()
        self.lyric_timer.stop()
        self.is_started = False
        print('Pause')
        self.ui.btn_play.setToolTip('Play')
        self.ui.btn_play.setStyleSheet("image: url(images/play.png);")


    def initialize_lyrics(self):
        self.lyric_time_index = 0
        self.ui.lyric_listWidget.clear()
        lrc_dict = self.song_selected.get_lyrics_dictionary()
        self.lyric_time_list = list(lrc_dict.keys())

        if len(self.lyric_time_list) != 0:
            for lrc_time in self.lyric_time_list:
                lrc_output = lrc_dict[lrc_time][0]
                item = QListWidgetItem(lrc_output)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.lyric_listWidget.addItem(item)
        else:
            item = QListWidgetItem('There are no lyrics')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.lyric_listWidget.addItem(item)

    """networking part"""
    def update_received_song_list(self, song_list):
        self.received_song_list = self.filter_remote_songs(song_list)

        # Execute the UI update on the main thread
        QtCore.QTimer.singleShot(0, lambda: self.add_received_songs(self.received_song_list))

    def filter_remote_songs(self, song_list):
        local_song_paths = set(self.local_path_list)

        filtered_songs = []
        for item in song_list:
            file_path = item['path']
            file_name = os.path.basename(file_path)
            local_file_path = os.path.join(self.directory_path, file_name)

            if local_file_path not in local_song_paths:
                filtered_songs.append(item)

        return filtered_songs

    def add_received_songs(self, song_list):
        if not song_list:
            return
        local_song_paths = set(self.local_path_list)
        for item in song_list:
            file_path = item['path']
            file_name = os.path.basename(file_path)
            local_file_path = os.path.normpath(os.path.join(self.directory_path, file_name))
            if local_file_path not in [os.path.normpath(x) for x in local_song_paths] and file_name not in self.all_received_song_list:
                icon_path = "images/cloud.png"
                icon = QIcon(icon_path)
                item_text = file_name
                item_w = QListWidgetItem()
                item_w.setText(item_text)
                item_w.setIcon(icon)
                self.ui.playlist_listWidget.addItem(item_w)
                self.all_received_song_list.append(file_name)
                self.song_path_list.append({
                    'index': self.local_songs_count,
                    'path': file_name,
                    'is_local': False
                })
                self.local_songs_count += 1

    def update_merged_song_list(self, received_song_list):
        # Merge the received song list with the local song list
        for song in received_song_list:
            song_is_new = True
            for local_song in self.song_path_list:
                if os.path.basename(song['path']) == os.path.basename(local_song['path']):
                    song_is_new = False
                    break
            if song_is_new:
                song['is_local'] = False
                song['path'] = os.path.basename(song['path'])
                self.song_path_list.append(song)

        # Update the user interface or any other components that depend on the song list
        # For example, if you have a listbox displaying the songs, you should update it here
        self.update_song_list_ui()


    def update_song_list_ui(self):
        self.select_songs(self.current_search_text)

    def initialize_song_data(self):
        self.song_selected = Song(self.song_current_path)
        self.initialize_lyrics()
        self.ui.label_pic.clear()
        pix = QPixmap()
        pix.loadFromData(self.song_selected.cover)
        self.ui.label_pic.setPixmap(pix)
        self.ui.label_pic.setScaledContents(True)

        self.ui.AudioInfo_listWidget.clear()
        self.ui.label_name.setText(self.song_selected.title)
        print("path", self.song_selected.path)

        self.vis_label = QtWidgets.QLabel()
        self.vis_label.setText("Visualization")
        self.vis_label.setStyleSheet("color: white; font: 18pt; font-weight:bold")
        self.vis_label.setAlignment(QtCore.Qt.AlignCenter)

        if not hasattr(self, "audio_visualizer"):
            self.vis_layout = QtWidgets.QVBoxLayout(self.ui.widget_vis)
            self.vis_layout.setObjectName("visualization")
            self.audio_visualizer = AudioVisualizer(self.song_selected.path)
            self.audio_visualizer.setMinimumSize(QtCore.QSize(300, 300))
            self.audio_visualizer.setGeometry(QtCore.QRect(0, 0, 300, 300))
            self.vis_layout.addWidget(self.vis_label)
            self.vis_layout.addWidget(self.audio_visualizer)
        else:
            self.audio_visualizer.update_audio_file(self.song_selected.path)

        self.setWindowTitle(self.song_selected.title + ' - ' + self.song_selected.artist + ' - LrcMusicPlayer')

        self.ui.AudioInfo_listWidget.setItemAlignment(QtCore.Qt.AlignCenter)

        self.ui.title_item = QListWidgetItem()
        self.ui.title_widget = QWidget()
        self.ui.title_layout = QtWidgets.QHBoxLayout()
        self.ui.title_label = QLabel("Title:")
        self.ui.title_edit = QLineEdit(self.song_selected.title)
        self.ui.title_label.setStyleSheet("color: white; font: 12pt; padding: 0;")
        with open('styles/lineEdit.css', 'r') as f:
            style_lineEdit = f.read()
        self.ui.title_edit.setStyleSheet((style_lineEdit))
        self.ui.title_edit.setFixedWidth(400)
        self.ui.title_edit.setFixedHeight(20)
        self.ui.title_edit.textChanged.connect(lambda text: setattr(self.song_selected, 'title', text))
        self.ui.title_layout.addWidget(self.ui.title_label)
        self.ui.title_layout.addWidget(self.ui.title_edit)
        self.ui.title_layout.setSpacing(0)
        self.ui.title_widget.setLayout(self.ui.title_layout)
        self.ui.title_item.setSizeHint(self.ui.title_widget.sizeHint())
        self.ui.AudioInfo_listWidget.addItem(self.ui.title_item)
        self.ui.AudioInfo_listWidget.setItemWidget(self.ui.title_item, self.ui.title_widget)

        self.ui.artist_item = QListWidgetItem()
        self.ui.artist_widget = QWidget()
        self.ui.artist_layout = QtWidgets.QHBoxLayout()
        self.ui.artist_label = QLabel("Artist:")
        self.ui.artist_edit = QLineEdit(self.song_selected.artist)
        self.ui.artist_label.setStyleSheet("color: white; font: 12pt; padding: 0;")
        with open('styles/lineEdit.css', 'r') as f:
            style_lineEdit = f.read()
        self.ui.artist_edit.setStyleSheet((style_lineEdit))
        self.ui.artist_edit.setFixedWidth(400)
        self.ui.artist_edit.setFixedHeight(20)
        self.ui.artist_edit.textChanged.connect(lambda text: setattr(self.song_selected, 'artist', text))
        self.ui.artist_layout.addWidget(self.ui.artist_label)
        self.ui.artist_layout.addWidget(self.ui.artist_edit)
        self.ui.artist_layout.setSpacing(0)
        self.ui.artist_widget.setLayout(self.ui.artist_layout)
        self.ui.artist_item.setSizeHint(self.ui.artist_widget.sizeHint())
        self.ui.AudioInfo_listWidget.addItem(self.ui.artist_item)
        self.ui.AudioInfo_listWidget.setItemWidget(self.ui.artist_item, self.ui.artist_widget)

        self.ui.album_item = QListWidgetItem()
        self.ui.album_widget = QWidget()
        self.ui.album_layout = QtWidgets.QHBoxLayout()
        self.ui.album_label = QLabel("Album:")
        self.ui.album_edit = QLineEdit(self.song_selected.album)
        self.ui.album_label.setStyleSheet("color: white; font: 12pt; padding: 0;")
        with open('styles/lineEdit.css', 'r') as f:
            style_lineEdit = f.read()
        self.ui.album_edit.setStyleSheet(style_lineEdit)
        self.ui.album_edit.setFixedWidth(400)
        self.ui.album_edit.setFixedHeight(20)
        self.ui.album_edit.textChanged.connect(lambda text: setattr(self.song_selected, 'album', text))
        self.ui.album_layout.addWidget(self.ui.album_label)
        self.ui.album_layout.addWidget(self.ui.album_edit)
        self.ui.album_layout.setSpacing(0)
        self.ui.album_widget.setLayout(self.ui.album_layout)
        self.ui.album_item.setSizeHint(self.ui.album_widget.sizeHint())
        self.ui.AudioInfo_listWidget.addItem(self.ui.album_item)
        self.ui.AudioInfo_listWidget.setItemWidget(self.ui.album_item, self.ui.album_widget)

        btn_item = QListWidgetItem()
        btn_widget = QWidget()
        btn_layout = QtWidgets.QHBoxLayout()
        save_info_btn = QtWidgets.QPushButton("Save Changes")
        save_info_btn.setStyleSheet(
            "background:rgb(245, 36, 67);border-radius:5px;font: 9pt;color: rgb(255, 250, 232);font-weight:bold")
        save_info_btn.setFixedWidth(150)
        save_info_btn.setFixedHeight(30)
        btn_layout.addWidget(save_info_btn, alignment=QtCore.Qt.AlignCenter)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(btn_layout)
        btn_item.setSizeHint(btn_widget.sizeHint())
        self.ui.AudioInfo_listWidget.addItem(btn_item)
        self.ui.AudioInfo_listWidget.setItemWidget(btn_item, btn_widget)

        # bind button to method
        save_info_btn.clicked.connect(lambda: EditFile.edit_audio_details(self, self.song_selected))

        print(self.song_selected)
        if self.song_selected.bits_per_sample == 0:
            self.ui.label_info.setText(
                f'{round(self.song_selected.sample_rate / 1000, 1)} kHz / '
                f'{self.song_selected.audio_type}'
            )
        else:
            self.ui.label_info.setText(
                f'{round(self.song_selected.sample_rate / 1000, 1)} kHz / '
                f'{self.song_selected.bits_per_sample} bits / '
                f'{self.song_selected.audio_type}'
            )


class DBThread(QtCore.QThread):
    stop_signal = QtCore.pyqtSignal()
    item_signal = QtCore.pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.folder_path = ''

    def run(self):
        self.create_songs_table()

    def process_file(self, current_file_path, current_file_name):
        file_extension = current_file_path.split('.')[-1].lower()
        allowed_extensions = ['wav', 'wave', 'mp3']
        if file_extension not in allowed_extensions:
            return

        song_instance = Song(current_file_path)
        insert_query = """
        insert into music_info (file_name, path, title, artist, album, date, genre, mtime, ctime) 
        values (?,?,?,?,?,?,?,?,?)
        """
        modification_time = int(os.path.getmtime(current_file_path))
        creation_time = int(os.path.getctime(current_file_path))
        query_params = (current_file_name, song_instance.path, song_instance.title,
                        song_instance.artist, song_instance.album, song_instance.date,
                        song_instance.genre, modification_time, creation_time)

        return insert_query, query_params
    
    def create_songs_table(self):
        with SqliteDB() as db:
            db.cursor.execute("DROP TABLE IF EXISTS music_info")
            db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS music_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT, path TEXT, title TEXT, artist TEXT, album TEXT, date TEXT, genre TEXT,
            mtime INT, ctime INT
            )""")

            file_count = 0
            for root, dirs, files in os.walk(self.directory_path):
                for file in files:
                    current_file_path = f'{root}/{file}'
                    current_file_name = os.path.splitext(file)[0]

                    result = self.process_file(current_file_path, current_file_name)
                    if result:
                        query, params = result
                        db.cursor.execute(query, params)
                        file_count += 1
                        self.item_signal.emit(file_count)
        self.stop_signal.emit()

