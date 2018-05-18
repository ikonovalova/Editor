from PyQt5 import QtCore, QtGui, QtWidgets


class Highlighter:
    # For text highlighting
    def highlightText(self, start, end, lineColor):

        c = self.textCursor()

        c.setPosition(start, QtGui.QTextCursor.MoveAnchor)
        c.setPosition(end, QtGui.QTextCursor.KeepAnchor)

        extraSelections = []
        selection = QtWidgets.QTextEdit.ExtraSelection()
        selection.format.setBackground(lineColor)
        selection.cursor = c

        extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

        # Move the cursor to the found location
        c.setPosition(end)
        self.setTextCursor(c)