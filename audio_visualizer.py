import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
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

        # Initialize the main window
        self.setWindowTitle("Audio Visualizer")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and a vertical layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a matplotlib figure and canvas
        self.figure = Figure()
        # Create a matplotlib figure and canvas
        color = QColor(0, 0, 32)
        r, g, b, _ = color.getRgb()
        self.figure.patch.set_facecolor((r/255, g/255, b/255))

        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

       # Create an axis for the plot
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylim(-1, 1)          # Set y-axis limits
        self.ax.set_xlim(0, self.blocksize)   # Set x-axis limits
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_frame_on(False)
        self.line, = self.ax.plot(np.zeros(self.blocksize), color='red')
        # Create an animation for updating the plot
        self.ani = animation.FuncAnimation(self.figure, self.audio_callback, frames=self.total_frames(),
                                           repeat=False, blit=False, interval=0)
        
    def total_frames(self):
        return len(self.data) // self.blocksize

    def audio_callback(self, frame):
        # Get the current block of audio data
        start = frame * self.blocksize
        end = (frame + 1) * self.blocksize
        block = self.data[start:end, 0]

        # Update the plot with the latest audio data
        self.line.set_ydata(block)
        self.canvas.draw()


