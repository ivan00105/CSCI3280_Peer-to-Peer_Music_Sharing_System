from music_player import MusicPlayer
from PyQt5 import QtWidgets
import sys
import threading

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    music_player = MusicPlayer()
    threading.Thread(target=music_player.peer.start_server).start()  # Start the server in a separate thread
    music_player.show()
    sys.exit(app.exec_())