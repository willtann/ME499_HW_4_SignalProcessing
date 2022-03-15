from slider import SliderDisplay
from PyQt5.QtWidgets import QApplication, QMainWindow,QDoubleSpinBox, QWidget, QVBoxLayout, QTextEdit,QHBoxLayout, QPushButton, QLineEdit, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as plt
import numpy as np
from digital_signal import DigitalSignal


class GUI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.mydata = None
        self.setWindowTitle('Interactive Bandpass Filter')
        self.setFixedSize(800, 500)
        self.nyquist = 5000

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
        self.low = SliderDisplay("Low: ", 0, self.nyquist, units='Hz')
        self.high = SliderDisplay("High: ", 0, self.nyquist, units='Hz')
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
        print(self.mydata.source_data)
        self.nyquist = self.mydata.sampling_frequency / 2

        self.mydata.start = self.start_entry.value()
        self.mydata.end = self.end_entry.value()
        self.mydata.low = self.low.curr_val
        self.mydata.high = self.high.curr_val
        self.mydata.subset_signal(self.mydata.start, self.mydata.end)
        self.mydata.bandpass(self.mydata.low, self.mydata.high)

        print(self.mydata.subset_signal())
        print(self.mydata.subset)

    def graph(self):
        self.draw(len(self.mydata.subset) / self.mydata.sampling_frequency)

    def draw(self, data):
        self.figure.clear()
        # """ Place holders """
        ax = self.figure.add_subplot(111)
        ax.plot(data, self.mydata.subset_signal())
        self.display.draw()

    def save(self):
        self.mydata.save_wav(filename=self.save_name.text(), start=self.mydata.start, end=self.mydata.end)


if __name__ == '__main__':
    app = QApplication([])
    gui = GUI()
    gui.show()
    # print(gui.draw)
    app.exec_()
