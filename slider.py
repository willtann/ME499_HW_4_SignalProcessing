#!/usr/bin/env python3


from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt


class SliderDisplay(QWidget):
    def __init__(self, name, low, high, ticks=1000, units=''):
        QWidget.__init__(self)
        self.curr_val = 0
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.name = name + " : {:0.3f}"
        self.low = low
        self.high = high
        self.units = units
        self.ticks = ticks

        """ Value label """
        self.label = QLabel(self.name.format(0) + self.units)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        """ Adding slider """
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, ticks)
        self.slider.valueChanged.connect(self.current_label)
        self.slider.valueChanged[int].connect(self.input_eq)
        layout.addWidget(self.slider)

    def current_label(self, value):
        """Return the current value of the slider"""
        # Converting from tick value to value in given range
        value = (value/self.ticks)*(self.high-self.low)
        self.label.setText(self.name.format(value) + self.units)
        return self.label

    def input_eq(self, value):
        self.curr_val = (value/self.ticks)*(self.high - self.low)
        return self.curr_val


if __name__ == '__main__':
    app = QApplication([])

    slider = SliderDisplay('foo', 0, 1, units='dB')

    slider.show()

    app.exec_()