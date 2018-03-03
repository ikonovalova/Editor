import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import json
import os


# class Main(QtWidgets.QMainWindow):
class Main(QtWidgets.QWidget):

    def __init__(self, parent=None):
        # QtWidgets.QMainWindow.__init__(self, parent)
        super(Main,self).__init__()

        # Rigthr layout for json
        self.j_tree = QtWidgets.QTextEdit()
        self.j_annot = QtWidgets.QTextEdit()

        # Left layout for text doc
        self.text_doc = QtWidgets.QPlainTextEdit()

        self.filename = "", ""  # ! dluciv

        self.initUI()

    def initUI(self):
        #Common Form
        hbox = QtWidgets.QVBoxLayout()

        # Rigthr layout for json
        # j_tree = QtWidgets.QTextEdit()
        # j_annot = QtWidgets.QTextEdit()

        # Left layout for text doc
        #  text_doc = QtWidgets.QTextEdit()

        # Create a vert. splitter
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(self.j_tree)
        splitter1.addWidget(self.j_annot)
        splitter1.setSizes([200,100])

        # Create a horiz. splitter
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.text_doc)
        splitter2.addWidget(splitter1)

        # Create an open button
        open_btn = QtWidgets.QPushButton("Open", self)
        open_btn.setFixedSize(100,30)
        # Connection
        open_btn.clicked.connect(self.open)

        hbox.addWidget(open_btn)
        hbox.addWidget(splitter2)

        self.setLayout(hbox)

        self.setWindowTitle("Writer")

        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def new(self):

        spawn = Main(self)
        spawn.show()


    def open(self):

        # Get filename and show only .txt files
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".", " (*.txt)")
        # Get filename without .txt
        self.j_tree = os.path.splitext(self.filename[0])
        # Ghange name
        self.j_tree = self.j_tree[0] + "1.txt" , "(*.txt)"
        #
#Не работает чтение из второго файла
        if self.filename:
            with open(self.filename[0], "r+") as file, open(self.j_tree[0], "r+") as j_file: # ! dluciv
                self.text_doc.setPlainText(file.read())
                self.j_tree.setPlainText(j_file.read())
                # json.JSONDecoder.decode()


def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()


    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

