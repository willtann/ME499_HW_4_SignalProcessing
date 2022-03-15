from slider import SliderDisplay
from PyQt5.QtWidgets import QApplication, QMainWindow,QDoubleSpinBox, QWidget, QVBoxLayout, QTextEdit,QHBoxLayout, QPushButton, QLineEdit, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as plt
import numpy as np
import wave, sys
from digital_signal import DigitalSignal


class GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.end = None
        self.start = None
        self.filtered_data = None
        self.subset_signal = None
        self.freq_high = None
        self.freq_low = None
        self.sampling_frequency = None
        self.source_data = None
        self.mydata = None
        self.nyquist = None
        self.start_entry = 0
        self.end_entry = None
        self.setWindowTitle('Interactive Bandpass Filter')
        self.setFixedSize(800, 500)

        # Load File
        load_layout = QHBoxLayout()
        self.input_filename = QLineEdit(self)
        load_button = QPushButton('Load')
        load_layout.addWidget(self.input_filename)
        load_layout.addWidget(load_button)
        load_button.clicked.connect(self.og_data)
        load_button.clicked.connect(self.graph)

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
        self.start_entry = QDoubleSpinBox(self)
        self.end_entry = QDoubleSpinBox(self)
        input_reset_layout.addWidget(QLabel("Start (s):"))
        input_reset_layout.addWidget(self.start_entry)
        input_reset_layout.addWidget(QLabel("End (s):"))
        input_reset_layout.addWidget(self.end_entry)
        self.start_entry.valueChanged.connect(self.og_data)
        self.end_entry.valueChanged.connect(self.og_data)
        self.start_entry.valueChanged.connect(self.graph)
        self.end_entry.valueChanged.connect(self.graph)



        # Save File
        save_layout = QHBoxLayout()
        self.save_name = QLineEdit(self)
        save_button = QPushButton('Save')
        save_layout.addWidget(self.save_name)
        save_layout.addWidget(save_button)
        save_button.clicked.connect(self.save)


        # Add Widgets
        top_level_layout.addWidget(self.display)
        top_level_layout.addLayout(slider_layout)
        top_level_layout.addLayout(input_reset_layout)
        top_level_layout.addLayout(load_layout)
        top_level_layout.addLayout(save_layout)


    def og_data(self):
        self.mydata = DigitalSignal.from_wav(self.input_filename.text())
        self.filtered_data = self.mydata.bandpass(self.low.curr_val, self.high.curr_val)
        self.sampling_frequency = self.mydata.sampling_frequency
        self.source_data = self.mydata.source_data
        self.nyquist = self.mydata.sampling_frequency/2
        self.start = self.start_entry.value()
        self.end = self.end_entry.value()
        self.freq_low = 0
        self.freq_high = self.nyquist
        self.subset_signal = self.mydata.subset_signal(self.start, self.end)

    def graph(self):
        self.draw(len(self.subset_signal))

    def draw(self, data):
        self.figure.clear()
        """ Place holders """
        ax = self.figure.add_subplot(111)
        """ plot data vs equation with parameters """
        ax.plot(len(self.subset_signal)/self.sampling_frequency,self.subset_signal)
        ax.set_xlim([self.start, self.end])  # g
        ax.set_ylim([min(self.subset_signal), max(self.subset_signal)])
        """ Fill custom title """
        # ax.set_title('{}'.format(self.textbox.text()))
        # ax.set_xlabel('x[rad]')
        # ax.set_ylabel('sin(x)')
        self.display.draw()

        # self.subset = self.mydata.subset_signal(self.start, self.end)

    def save(self):
        self.mydata.save_wav(filename=self.save_name.text(), start=self.start, end=self.end)

    # def refresh(self):
    #     self.filtered_data = DigitalSignal.bandpass(self.low.curr_val, self.high.curr_val)


if __name__ == '__main__':
    app = QApplication([])
    gui = GUI()
    gui.show()
    # print(gui.draw)
    app.exec_()
