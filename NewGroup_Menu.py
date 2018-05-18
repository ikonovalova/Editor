import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import json


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

# Add the new selected group into the json file
class NewGroup_Menu(QtWidgets.QWidget):
    def __init__(self, cursor_data, loaded_data, path, start_elem, end_elem, parent):
        super().__init__()
        self.cursor_data  =  cursor_data
        self.data = loaded_data # json
        self.path = path  # current file
        self.start_elem = start_elem # the first selected element
        self.end_elem = end_elem # the last selected element
        self.parent = parent
        self.setWindowTitle("Add new group")
        vbox = QtWidgets.QVBoxLayout(self)
        hbox = QtWidgets.QHBoxLayout()
        save_btn = QtWidgets.QPushButton("Save", self)
        cancel_btn = QtWidgets.QPushButton("Cancel", self)
        hbox.addWidget(cancel_btn)

        hbox.addWidget(save_btn)
        save_btn.clicked.connect(self.add_newGroup)
        cancel_btn.clicked.connect(self.close)

        descr_text = QtWidgets.QLabel("Write annotation for the group")
        descr_text.setFixedSize(200,50)
        self.annot_text = QtWidgets.QPlainTextEdit()

        vbox.addWidget(descr_text)
        vbox.addWidget(self.annot_text)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    @try_except
    def add_newGroup(self, checked):
        print(checked)
        new_data ={}

        count_elem = len(self.data["Benchmarks"]) + 1
        new_data["name"] = str(count_elem)

        new_data["annotation"] = self.annot_text.toPlainText()

        new_data["group_ids"] = []
        new_we = {}
        new_we["name2"] = self.cursor_data

        count_dupl  = sum(len(dupl["group_ids"]) for dupl in self.data["Benchmarks"]) + 1
        new_we["id_dupl"] = count_dupl

        new_we["position"] = []
        add_pos = new_we["position"]
        add_pos.insert(0, self.start_elem)
        add_pos.insert(1,self.end_elem)

        new_data["group_ids"].append(new_we)

        self.data["Benchmarks"].append(new_data)

        self.parent.update_json_file(self.path, self.data)
        self.parent.load_groups( self.parent.data)
        self.close()