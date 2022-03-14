from slider import SliderDisplay
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit,QHBoxLayout, QPushButton, QLineEdit, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as plt
import numpy as np
import wave, sys
from digital_signal import DigitalSignal


class GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.subset = None
        self.freq_high = None
        self.freq_low = None
        self.sampling_frequency = None
        self.source_data = None
        self.mydata = None
        self.nyquist = None
        self.start = 0
        self.end = None
        self.setWindowTitle('Interactive Bandpass Filter')
        self.setFixedSize(800, 500)

        # Load File
        load_layout = QHBoxLayout()
        self.input_filename = QLineEdit(self)
        load_button = QPushButton('Load')
        load_layout.addWidget(self.input_filename)
        load_layout.addWidget(load_button)
        load_button.clicked.connect(self.og_data)

        # Layout
        widget = QWidget()
        self.setCentralWidget(widget)
        top_level_layout = QVBoxLayout()
        widget.setLayout(top_level_layout)

        # The display for the graph
        self.figure = Figure()
        self.display = FigureCanvas(self.figure)
        self.figure.clear()

        # Sliders
        slider_layout = QHBoxLayout()
        self.low = SliderDisplay("Low: ", 0, 5, units='Hz')
        self.high = SliderDisplay("High: ", 0, 5, units='Hz')
        slider_layout.addWidget(self.low)
        slider_layout.addWidget(self.high)

        # Start-End values and reset button
        input_reset_layout = QHBoxLayout()
        self.start = QLineEdit(self)
        self.end = QLineEdit(self)

        input_reset_layout.addWidget(QLabel("Start (s):"))
        input_reset_layout.addWidget(self.start)
        input_reset_layout.addWidget(QLabel("End (s):"))
        input_reset_layout.addWidget(self.end)

        # Save File
        save_layout = QHBoxLayout()
        self.save_name = QLineEdit(self)
        save_button = QPushButton('Save')
        save_layout.addWidget(self.save_name)
        save_layout.addWidget(save_button)
        save_button.clicked.connect(self.save)


        # Add Widgets
        # top_level_layout.addWidget(self.figure)
        top_level_layout.addLayout(slider_layout)
        top_level_layout.addLayout(input_reset_layout)
        top_level_layout.addLayout(load_layout)
        top_level_layout.addLayout(save_layout)

    def og_data(self):
        self.mydata = DigitalSignal.from_wav(self.input_filename.text())
        self.nyquist = self.mydata.nyquist_freq
        self.source_data = self.mydata.source_data
        self.sampling_frequency = self.mydata.sampling_frequency
        self.freq_low = self.mydata.freq_low
        self.freq_high = self.mydata.freq_high
        return print(DigitalSignal.from_wav(self.input_filename.text()))

    def save(self):
        self.subset = DigitalSignal.subset_signal(self.start, self.end)
        DigitalSignal.save_wav(self, filename=self.save_name.text(), start=self.start, end=self.end)

    # def subset(self):

if __name__ == '__main__':
    app = QApplication([])
    gui = GUI()
    gui.show()
    # print(gui.draw)
    app.exec_()
