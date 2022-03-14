#!/usr/bin/env python3
from slider import SliderDisplay
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class Grapher(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('Grapher')

        # Control buttons for the interface
        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(app.exit)

        graph_button = QPushButton('Graph')
        graph_button.clicked.connect(self.graph)

        # The display for the graph
        self.figure = Figure()
        self.display = FigureCanvas(self.figure)
        self.figure.clear()

        # The layout of the interface
        widget = QWidget()
        self.setCentralWidget(widget)

        """ Add Graph Button """
        top_level_layout = QHBoxLayout()
        widget.setLayout(top_level_layout)

        left_side_layout = QVBoxLayout()
        left_side_layout.addWidget(graph_button)

        """ Add Name """
        self.textbox = QLineEdit(self)
        left_side_layout.addWidget(self.textbox)

        """ Add Value Sliders """
        self.amplitude = SliderDisplay('Amplitude', 0, 5)
        left_side_layout.addWidget(self.amplitude)

        self.frequency = SliderDisplay('Frequency', 0, 5, units='Hz')
        left_side_layout.addWidget(self.frequency)

        self.phase = SliderDisplay('Phase Shift', 0, 1, units="rad")
        left_side_layout.addWidget(self.phase)

        """ Add Quit Button"""
        left_side_layout.addStretch()
        left_side_layout.addWidget(quit_button)

        """ Add Plot window """
        top_level_layout.addLayout(left_side_layout)
        top_level_layout.addWidget(self.display)

    def graph(self):
        self.draw(np.linspace(0, 2*np.pi, 1000))

    def draw(self, data):
        self.figure.clear()
        """ Place holders """
        a = self.amplitude.curr_val
        f = self.frequency.curr_val
        p = self.phase.curr_val
        ax = self.figure.add_subplot(111)
        """ plot data vs equation with parameters """
        ax.plot(data, a*np.sin(2*f*np.pi*(data-p)))
        ax.set_xlim([0, 5])  # g
        ax.set_ylim([-5, 5])
        """ Fill custom title """
        ax.set_title('{}'.format(self.textbox.text()))
        ax.set_xlabel('x[rad]')
        ax.set_ylabel('sin(x)')
        self.display.draw()


if __name__ == '__main__':
    app = QApplication([])
    gui = Grapher()
    print(gui.draw)
    gui.show()
    app.exec_()