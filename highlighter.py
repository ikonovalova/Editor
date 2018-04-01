from PyQt5 import QtCore, QtGui, QtWidgets


class Highlighter:
    # For text highlighting
    def highlightText(self, start, end, lineColor):
        # colorFormat =  QtGui.QTextCharFormat()
        # colorFormat.setBackground(QtGui.QColor(QtCore.Qt.green).lighter(160))

        c = self.textCursor()

        c.setPosition(start, QtGui.QTextCursor.MoveAnchor)
        c.setPosition(end, QtGui.QTextCursor.KeepAnchor)

        # c.mergeCharFormat(colorFormat)
        # c.setPosition(end)
        # self.setTextCursor(c)

        extraSelections = []
        selection = QtWidgets.QTextEdit.ExtraSelection()
        # lineColor = QtGui.QColor(QtCore.Qt.green).lighter(160)
        selection.format.setBackground(lineColor)
        selection.cursor = c

        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

        # Move the cursor to the found location
        c.setPosition(end)
        self.setTextCursor(c)