from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout


class Interface(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('window name here')

        self.count=0
        # A widget to hold everything
        widget = QWidget()
        self.setCentralWidget(widget)

        # A layout
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # A button to quit out of the app
        quit_button = QPushButton('Quit')
        quit_button.clicked.connect(app.exit)

        # A button to print the current counter
        print_button = QPushButton("Print")
        print_button.clicked.connect(self.printer)

        # text box input for setting the counter
        self.textbox = QLineEdit(self)

        # ok button to set the counter
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.setval)

        # Add things to the layout
        layout.addWidget(quit_button)
        layout.addWidget(print_button)
        layout.addWidget(self.textbox)
        layout.addWidget(ok_button)


    def printer(self):
        print(self.count)
        self.count += 1

    #set the counter from the text box
    def setval(self):
        val = self.textbox.text()
        self.count = int(val)
        self.textbox.clear()


if __name__ == '__main__':
    app = QApplication([])

    interface = Interface()

    interface.show()

    app.exec_()
