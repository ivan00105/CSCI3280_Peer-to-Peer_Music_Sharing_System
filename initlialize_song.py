from PyQt5 import QtWidgets
from player_window import UI_MainWindow
from decode import Song
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt, QUrl, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5 import QtCore
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QLabel, QLineEdit, QVBoxLayout, QLabel, QLineEdit, QListWidget
from pypinyin import lazy_pinyin, Style
from PyQt5.QtGui import QColor
from audio_visualizer import AudioVisualizer
from edit_song_details import EditFile

class InitializeData(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = UI_MainWindow()
        self.ui.buildUiElements(self)

    def song_data_init(self, song_now_path):
        song_selected = Song(song_now_path)

        self.song_lrc_init(song_selected)

        self.ui.label_pic.clear()
        pix = QPixmap()
        pix.loadFromData(song_selected.cover)
        self.ui.label_pic.setPixmap(pix)
        self.ui.label_pic.setScaledContents(True)

        self.ui.AudioInfo_listWidget.clear()
        self.ui.label_name.setText(song_selected.title)
        print("path", song_selected.path)


        self.vis_label = QtWidgets.QLabel()
        self.vis_label.setText("Visualization")
        self.vis_label.setStyleSheet("color: white; font: 18pt;")

        self.vis_label_box = QtWidgets.QVBoxLayout(self.ui.widget_vis)
        self.vis_label_box.addWidget(self.vis_label)

        self.vis_layout = QtWidgets.QVBoxLayout(self.ui.widget_vis)
        self.vis_layout.setObjectName("visualization")
        self.audio_visualizer = AudioVisualizer(song_selected.path)
        self.audio_visualizer.setMinimumSize(QtCore.QSize(300, 300))
        self.audio_visualizer.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.vis_layout.addWidget(self.audio_visualizer)

        self.setWindowTitle(song_selected.title + ' - ' + song_selected.artist + ' - LrcMusicPlayer')
        self.ui.AudioInfo_listWidget.setStyleSheet(
            "QListWidget::item { padding: 5px; color:white; border-radius: 5px; align:center}")
        self.ui.AudioInfo_listWidget.setItemAlignment(QtCore.Qt.AlignCenter)

        title_item = QListWidgetItem()
        self.ui.AudioInfo_listWidget.addItem('Title')
        title_edit = QLineEdit(song_selected.title)
        title_edit.setStyleSheet(
            "QLineEdit{"
            "    border:1px groove white;"
            "    border-radius:2px;"
            '    font: 12pt;'
            '    color: white;'
    
            "}"
        )
        title_edit.setFixedWidth(250)
        title_edit.setFixedHeight(25)
        # title_edit.setAlignment(QtCore.Qt.AlignCenter)
        title_edit.textChanged.connect(lambda text: setattr(song_selected, 'title', text))
        self.ui.AudioInfo_listWidget.addItem(title_item)
        self.ui.AudioInfo_listWidget.setItemWidget(title_item, title_edit)

        artist_item = QListWidgetItem()
        # artist_layout = QtWidgets.QHBoxLayout()
        self.ui.AudioInfo_listWidget.addItem('Artist')
        artist_edit = QLineEdit(song_selected.artist)
        artist_edit.setStyleSheet(
            "QLineEdit{"
            "    border:1px groove white;"
            "    border-radius:2px;"
            '    font: 12pt;'
            '    color: white;'
    
            "}"
        )
        artist_edit.setFixedWidth(250)
        artist_edit.setFixedHeight(25)
        artist_edit.textChanged.connect(lambda text: setattr(song_selected, 'artist', text))
        self.ui.AudioInfo_listWidget.addItem(artist_item)
        self.ui.AudioInfo_listWidget.setItemWidget(artist_item, artist_edit)

        album_item = QListWidgetItem()
        album_edit = QLineEdit(song_selected.album)
        self.ui.AudioInfo_listWidget.addItem('Album')
        album_edit.setStyleSheet(
            "QLineEdit{"
            "    border:1px groove white;"
            "    border-radius:2px;"
            '    font: 12pt;'
            '    color: white;'
    
            "}"
        )
        album_edit.setFixedWidth(250)
        album_edit.setFixedHeight(25)
        album_edit.textChanged.connect(lambda text: setattr(song_selected, 'album', text))
        self.ui.AudioInfo_listWidget.addItem(album_item)
        self.ui.AudioInfo_listWidget.setItemWidget(album_item, album_edit)

        btn_item = QListWidgetItem()
        save_info_btn = QtWidgets.QPushButton("Save")
        self.ui.AudioInfo_listWidget.addItem("")
        save_info_btn.setStyleSheet(
            "QPushButton{"
            "   background:rgb(245, 36, 67);"
            "    border-radius:0px;"
            '    font: 9pt;'
            "    color: rgb(255, 250, 232);"
            "}"
            "QPushButton:hover{"
            "    background:white;"
            "color: rgb(0,0,32)"
            "}"
            ""
        )
        save_info_btn.setFixedWidth(250)
        save_info_btn.setFixedHeight(25)
        self.ui.AudioInfo_listWidget.addItem(btn_item)
        self.ui.AudioInfo_listWidget.setItemWidget(btn_item, save_info_btn)

        # bind button to method
        save_info_btn.clicked.connect(lambda: EditFile.edit_audio_details(self, song_selected))

        print(song_selected)
        if song_selected.bits_per_sample == 0:
            self.ui.label_info.setText(
                f'{round(song_selected.sample_rate / 1000, 1)} kHz / '
                f'{song_selected.audio_type}'
            )
        else:
            self.ui.label_info.setText(
                f'{round(song_selected.sample_rate / 1000, 1)} kHz / '
                f'{song_selected.bits_per_sample} bits / '
                f'{song_selected.audio_type}'
            )



    def song_lrc_init(self, song_selected):
        self.lrc_time_index = 0
        self.ui.lyric_listWidget.clear()
        lrc_dict = song_selected.get_lyrics_dictionary()
        print(lrc_dict)
        self.lrc_time_list = list(lrc_dict.keys())
        
        if len(self.lrc_time_list) != 0:
            for lrc_time in self.lrc_time_list:
                lrc_output = lrc_dict[lrc_time][0]

                item = QListWidgetItem(lrc_output)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.ui.lyric_listWidget.addItem(item)
        else:
            item = QListWidgetItem('There are no lyrics')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.ui.lyric_listWidget.addItem(item)
