#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import os
from PyQt5 import QtCore, QtGui, QtWidgets
import json

from TextEditor import TextEditor  # for number of line
from NewGroup_Menu import NewGroup_Menu  # for Adding new group
from find import Find  # for find user text
from highlighter import Highlighter  # for colored cursor text


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


# class Main(QtWidgets.QMainWindow):
class Main(QtWidgets.QWidget):

    def __init__(self, parent=None):
        # QtWidgets.QMainWindow.__init__(self, parent)
        super(Main, self).__init__()

        # Right layout for json
        self.j_tree = QtWidgets.QTreeView()
        # self.j_annot = QtWidgets.QTreeView()
        self.j_annot = QtWidgets.QPlainTextEdit()

        # Left layout for text doc
        # self.text_doc = QtWidgets.QPlainTextEdit()
        self.text_doc = TextEditor()

        self.filename = None
        self.bmks_filename = None
        self.data = None

        self.initUI()

        # Open the annotation
        self.j_tree.clicked.connect(self.openElement)

        # Show cursor pos
        self.j_tree.clicked.connect(self.load_cursorPos)

        # Find the text
        self.findAction = QtWidgets.QAction(self)
        self.findAction.setShortcut('Ctrl+F')
        self.findAction.triggered.connect(Find(self).show)
        self.addAction(self.findAction)

    @try_except
    def initUI(self):
        # Common Form
        hbox = QtWidgets.QVBoxLayout()
        bbox = QtWidgets.QHBoxLayout()

        # Create a vert. splitter
        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        splitter1.addWidget(self.j_tree)
        splitter1.addWidget(self.j_annot)
        splitter1.setSizes([200, 100])

        # Create a horiz. splitter
        splitter2 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.text_doc)
        splitter2.addWidget(splitter1)

        # Create an open button
        open_btn = QtWidgets.QPushButton("Open", self)
        open_btn.setFixedSize(100, 30)
        report_btn = QtWidgets.QPushButton("Report", self)
        report_btn.setFixedSize(100, 30)

        # Connection
        open_btn.clicked.connect(self.open)
        report_btn.clicked.connect(self.report)

        bbox.addWidget(open_btn)
        bbox.addWidget(report_btn)

        hbox.addLayout(bbox)
        hbox.addWidget(splitter2)



        self.setLayout(hbox)

        # Menu by right click
        self.text_doc.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.text_doc.customContextMenuRequested.connect(self.menu_my)

        self.setWindowTitle("Writer")

        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    # Menu by right click
    def menu_my(self):
        menu = QtWidgets.QMenu(self)

        new_group = self.add_Menu
        menu.addAction("Add new group", new_group)
        to_group = self.To_Group
        menu.addAction("Add to current group", to_group)

        menu.exec_(QtGui.QCursor.pos())

    # Add new group
    @try_except
    def add_Menu(self):
        dd = self.text_doc.textCursor().selectedText()  # cursor выделенное
        start_elem = self.text_doc.textCursor().selectionStart()  # the number of the first element of the selected text
        end_elem = self.text_doc.textCursor().selectionEnd()  # the number of the last element of the selected text

        self.dialog = NewGroup_Menu(dd, self.data, self.bmks_filename, start_elem, end_elem, self)
        self.dialog.show()

    # Add new into selected group
    @try_except
    def To_Group(self):
        dd = self.text_doc.textCursor().selectedText()  # the highlighted text
        start_elem = self.text_doc.textCursor().selectionStart()  # the number of the first element of the selected text
        end_elem = self.text_doc.textCursor().selectionEnd()  # the number of the last element of the selected text

        for text in self.data["Benchmarks"]:
            if text["name"] == self.item_data[1]:
                # index of the selected group
                ind = self.data["Benchmarks"].index(text)
                # insert new data into group
                new_d = {}
                new_d["name2"] = dd

                count_dupl = sum(len(dupl["group_ids"]) for dupl in self.data["Benchmarks"]) + 1
                new_d["id_dupl"] = count_dupl

                new_d["position"] = []
                add_pos = new_d["position"]
                add_pos.insert(0, start_elem)
                add_pos.insert(1, end_elem)

                self.data["Benchmarks"][ind]["group_ids"].insert(len(text["group_ids"])+1, new_d)

        self.update_json_file(self.bmks_filename, self.data)
        self.load_groups(self.data)

    @try_except
    def update_json_file(self, j_filename, data):
        with open(j_filename, 'w') as fp:
            json.dump(data, fp)

    @try_except
    def load_groups(self, elements):
        self.model.clear()

        for text in elements["Benchmarks"]:
            # item = QtGui.QStandardItem(text["name"])
            item = QtGui.QStandardItem(text["annotation"])
            item.setData([1, text["name"], 0])

            child = text["group_ids"]
            for test in child:
                new_elem = test["name2"]
                test1 = QtGui.QStandardItem(str(new_elem[0: 50]))  # читает только text  данные ?

                item.appendRow(test1)
                test1.setData([2, 0, test["id_dupl"]])

            self.model.appendRow(item)
            self.model.setHorizontalHeaderLabels([self.tr("Benchmarks")])

    @try_except
    def openElement(self, checked):
        print(checked)
        # Get the index of chosen element
        index = self.j_tree.currentIndex()
        # Get the name of chosen element(two var-ts)
        # item = QtCore.QModelIndex.data(index)
        # work = self.model.data(index)

        item = self.model.itemFromIndex(index)
        # Get the data that was put in item before
        self.item_data = QtGui.QStandardItem.data(item)
        # Get the name of clicked element
        self.item_text = QtGui.QStandardItem.text(item)

        if self.item_data[0] == 1:
            # load annotation
           # self.j_annot.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
           # self.model_annot = QtGui.QStandardItemModel()
            # self.load_annot(self.item_text, self.data)
            self.load_annot(self.item_data[1], self.data)

           # self.j_annot.setModel(self.model_annot)
           # self.model_annot.setHorizontalHeaderLabels([self.tr("Annotation")])

    def load_annot(self, check, elements):
        for text in elements["Benchmarks"]:
            elem = QtGui.QStandardItem(str(text["name"]))
            elem_text = QtGui.QStandardItem.text(elem)
            if elem_text == check:
                # annot = QtGui.QStandardItem(text["annotation"])
                # self.model_annot.appendRow(annot)
                self.j_annot.setPlainText(text["annotation"])

    @try_except
    def load_cursorPos(self, checked):
        print(checked)
        elements = self.data
        check = self.item_data[2]

        index = self.j_tree.currentIndex()
        item = self.model.itemFromIndex(index)
        item_data = QtGui.QStandardItem.data(item)
        self.item_text = QtGui.QStandardItem.text(item)

        for text in elements["Benchmarks"]:
            if item_data[0] == 2:
                for el in text["group_ids"]:
                    if el["id_dupl"] == check:
                        pos = el["position"]
                        start = pos[0]
                        end = pos[1]
                        # length = end - start

                        lineColor = QtGui.QColor(QtCore.Qt.red).lighter(160)
                        Highlighter.highlightText(self.text_doc, start, end, lineColor)

    @try_except  # если это писать перед функцией, то она перестанет вылетать молча
    def open(self, checked):
        print(checked)  # Этот аргумент есть у события clicked @try_except требует, чтобы все аргументы были описаны
        # Get filename and show only .txt files
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', ".", " (*.txt)")[0]

        if self.filename:
            # Бенчмарки всегда хранятся в файле <имя документа>.json
            self.bmks_filename = self.filename + '.json'
            with open(self.filename, "r+", encoding='utf-8') as file, open(self.bmks_filename, "r+", encoding='utf-8') as j_file:  # ! dluciv
                self.text_doc.setPlainText(file.read())
                self.data = json.load(j_file)

                # load groups
                self.j_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.model = QtGui.QStandardItemModel()
                self.load_groups(self.data)

                self.j_tree.setModel(self.model)
                self.model.setHorizontalHeaderLabels([self.tr("Benchmarks")])

    @try_except  # если это писать перед функцией, то она перестанет вылетать молча
    def report(self, checked):
        import subprocess
        def fixsep(path):
            return path.replace("\\", os.path.sep).replace("/", os.path.sep)

        fc2h = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "df_visual_report", "fuzzyclones2html.py"
        )

        subprocess.Popen([
            sys.executable, fc2h,
            '-jfrm', 'bench', '-ob', 'True',
            '-sx', fixsep(os.path.abspath(self.filename)),
            '-ndgj', fixsep(os.path.abspath(self.filename) + ".json")
        ])

def main():
    app = QtWidgets.QApplication(sys.argv)

    main = Main()
    main.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()