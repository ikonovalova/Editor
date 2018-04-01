from PyQt5 import QtCore, QtGui, QtWidgets
from highlighter import Highlighter

import re


def try_except(function):
    """
    https://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
    """
    import functools

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print("Exception in " + function.__name__ + ": " + repr(e))
            raise

    return wrapper


class Find(QtWidgets.QDialog):
    def __init__(self, parent=None):

        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent

        self.lastMatch = None

        self.initUI()

    def initUI(self):

        # Button to search the document for something
        findButton = QtWidgets.QPushButton("Find", self)
        findButton.clicked.connect(self.find)

        self.findField = QtWidgets.QTextEdit(self)
        self.findField.resize(250, 50)

        # Case Sensitivity option
        self.caseSens = QtWidgets.QCheckBox("Case sensitive", self)

        # Layout the objects on the screen
        layout = QtWidgets.QGridLayout()

        layout.addWidget(self.findField, 1, 0, 1, 4)
        layout.addWidget(findButton, 2, 0, 1, 2)

        # Add some spacing
        spacer = QtWidgets.QWidget(self)
        spacer.setFixedSize(0, 10)
        layout.addWidget(spacer, 5, 0)

        layout.addWidget(self.caseSens, 6, 1)

        self.setGeometry(300, 300, 360, 250)
        self.setWindowTitle("Find")
        self.setLayout(layout)

    @try_except
    def find(self, checked):
        print(checked)

        # Grab the parent's text
        text = self.parent.text_doc.toPlainText()

        # And the text to find
        query = self.findField.toPlainText()

        # By default regexes are case sensitive but usually a search isn't
        # case sensitive by default, so we need to switch this around here
        flags = 0 if self.caseSens.isChecked() else re.I

        # Compile the pattern
        pattern = re.compile(query, flags)

        # If the last match was successful, start at position after the last
        # match's start, else at 0
        start = self.lastMatch.start() + 1 if self.lastMatch else 0

        # The actual search
        self.lastMatch = pattern.search(text, start)

        if self.lastMatch:
            start = self.lastMatch.start()
            end = self.lastMatch.end()

            lineColor = QtGui.QColor(QtCore.Qt.green).lighter(160)
            Highlighter.highlightText(self.parent.text_doc, start, end, lineColor)

        else:
            # if the search was unsuccessful
            print("Nothing was found")
