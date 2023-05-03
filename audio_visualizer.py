import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtGui import QColor
import matplotlib.animation as animation
import numpy as np
import soundfile as sf
import matplotlib


# Set the backend to Qt5Agg
matplotlib.use('Qt5Agg')


class AudioVisualizer(QMainWindow):
    def __init__(self, audio_file):
        super(AudioVisualizer, self).__init__()

        # Load the audio file
        self.data, self.fs = sf.read(audio_file, dtype='float32')

        # Define the audio settings
        self.blocksize = 448  # Block size for visualizing
        self.frame = 0
        self.anim_running = True

        # Initialize the main window
        self.setWindowTitle("Audio Visualizer")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and a vertical layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a matplotlib figure and canvas
        self.figure = Figure()
        color = QColor(0, 0, 32)
        r, g, b, _ = color.getRgb()
        self.figure.patch.set_facecolor((r / 255, g / 255, b / 255))

        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        # Create a horizontal layout for the buttons
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # Create the stop button
        self.stop_button = QPushButton('Stop')
        self.stop_button.clicked.connect(self.stop_animation)
        self.button_layout.addWidget(self.stop_button)

        # Create the resume button
        self.resume_button = QPushButton('Resume')
        self.resume_button.clicked.connect(self.resume_animation)
        self.button_layout.addWidget(self.resume_button)

        # Create an axis for the plot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylim(-1, 1)  # Set y-axis limits
        self.ax.set_xlim(0, self.blocksize)  # Set x-axis limits
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_frame_on(False)
        self.line, = self.ax.plot(np.zeros(self.blocksize), color='green')
        # Create an animation for updating the plot
        self.ani = animation.FuncAnimation(self.figure, self.audio_callback, frames=self.total_frames(),
                                   repeat=False, blit=False, interval=10)

    def total_frames(self):
        return len(self.data) // self.blocksize

    def update_audio_file(self, audio_file):
        # Load the new audio file
        self.data, self.fs = sf.read(audio_file, dtype='float32')

        # Reset the animation
        self.anim_running = True
        if self.ani.event_source is not None:
            self.ani.event_source.start()

    def audio_callback(self, frame):
        if not self.anim_running:
            return

        # Get the start and end indices of the current block of audio data
        start = frame * self.blocksize
        end = start + self.blocksize

        # Get the audio data that corresponds to the current block
        block = self.data[start:end, 0]

        # Pad the block with zeros if its length is less than the blocksize
        if len(block) < self.blocksize:
            block = np.pad(block, (0, self.blocksize - len(block)))

        # Update the plot with the latest audio data
        self.line.set_ydata(block)
        self.canvas.draw()

        self.frame = frame

        # Check if the current frame is greater than or equal to the total number of frames
        if frame >= self.total_frames() - 1:
            self.stop_animation()

    def stop_animation(self):
        # print(str)
        # print("inside stop")
        self.anim_running = False
        if self.ani.event_source is not None:
            self.ani.event_source.stop()

    def resume_animation(self):
        # print("Resume animation called")
        self.anim_running = True
        # print(self.anim_running)
        if self.ani.event_source is not None:
            self.ani.event_source.start()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     audio_file = "H:/P2P/test/CSCI3280Project/Music_Player/music/numb.wav"
#     window = AudioVisualizer(audio_file)
#     window.show()
#     sys.exit(app.exec_())
