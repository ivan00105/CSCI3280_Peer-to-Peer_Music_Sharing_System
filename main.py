from music_player import MusicPlayer
from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) 
    music_player = MusicPlayer()
    music_player.show()
    sys.exit(app.exec_())
