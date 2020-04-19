#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Mirakyux"

# GUI viewer to view JSON data as tree.
# packages needed:
# python3-chardet
# python3-pyqt5

# Std
import argparse
import collections
import json
import sys
import datetime

# External
import chardet
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets

__conf__ = "./conf.json"

# 日志记录类
class Logger(object):
    def __init__(self, filename='default.log', stream=sys.stdout):
        self.terminal = stream
        self.log = open(filename, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(datetime.datetime.now().strftime('[%Y.%m.%d-%H:%M:%S] ') + message)

    def flush(self):
        pass
    
sys.stdout = Logger('console.log', sys.stdout)

# 树搜索类
class TextToTreeItem:

    def __init__(self):
        self.text_list = []
        self.titem_list = []

    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str in s:
                titem_list.append(self.titem_list[i])

        return titem_list


class JsonView(QtWidgets.QWidget):

    def __init__(self):
        super(JsonView, self).__init__()

        self.label_list = []
        self.label_disp = []
        self.label_child = ""

        self.load_conf()
        self.find_box = None
        self.tree_widget = None
        self.text_to_titem = TextToTreeItem()
        self.find_str = ""
        self.found_titem_list = []
        self.found_idx = 0

        jdata = ""

        # Find UI

        find_layout = self.make_find_ui()

        # Tree

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(self.label_disp)
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        # root_item = QtWidgets.QTreeWidgetItem(["Root"])
        # self.recurse_jdata(None, root_item)
        # self.tree_widget.addTopLevelItem(root_item)

        # Add table to layout

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tree_widget)

        # Group box

        gbox = QtWidgets.QGroupBox("Viewer")
        gbox.setLayout(layout)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(find_layout)
        layout2.addWidget(gbox)

        self.setLayout(layout2)

    # 加载配置文件
    def load_conf(self):
        try:
            with open(__conf__, 'rb') as f:
                cur_encoding = chardet.detect(f.read())['encoding']
            with open(__conf__, encoding=cur_encoding) as jfile:
                conf = json.load(jfile, object_pairs_hook=collections.OrderedDict)
        except Exception as e:
            print("Failed to load Conf.json. Use default")
            self.label_list = ["word", "definition"]
            self.label_disp = ["Key", "Value"]
            self.label_child = "child"
        else:
            print("Conf.json loaded successfully.")
            for key, val in conf["map"].items():
                self.label_disp.append(key)
                self.label_list.append(val)
            self.label_child = str(conf["child"])

    def make_find_ui(self):

        # Text box
        self.find_box = QtWidgets.QLineEdit()
        self.find_box.returnPressed.connect(self.find_button_clicked)

        # Find Button
        find_button = QtWidgets.QPushButton("Find")
        find_button.clicked.connect(self.find_button_clicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.find_box)
        layout.addWidget(find_button)

        return layout

    # 查找
    def find_button_clicked(self):

        find_str = self.find_box.text()

        # Very common for use to click Find on empty string
        if find_str == "":
            return

        # New search string
        if find_str != self.find_str:
            self.find_str = find_str
            self.found_titem_list = self.text_to_titem.find(self.find_str)
            self.found_idx = 0
        else:
            item_num = len(self.found_titem_list)
            self.found_idx = (self.found_idx + 1) % item_num

        self.tree_widget.setCurrentItem(self.found_titem_list[self.found_idx])


    # 解析json数据
    def recurse_jdata(self, jdata, tree_widget):
        label_row = []
        if isinstance(jdata, dict):
            for key in self.label_list:
                label_row.append(str(jdata.get(key, "")))
            self.tree_add_row(label_row, jdata.get(self.label_child, []), tree_widget)

        # if isinstance(jdata, dict):
        #     for key, val in jdata.items():
        #         self.tree_add_row(key, val, tree_widget)
        # elif isinstance(jdata, list):
        #     for i, val in enumerate(jdata):
        #         key = str(i)
        #         self.tree_add_row(key, val, tree_widget)
        else:
            print("This should never be reached!")

    # 添加行
    # def tree_add_row(self, key, val, tree_widget):
    def tree_add_row(self, text_list, childs, tree_widget):

        # text_list = []
        row_item = QtWidgets.QTreeWidgetItem(text_list)

        if isinstance(childs, list):
            for i, val in enumerate(childs):
                self.recurse_jdata(val, row_item)

        # if isinstance(val, dict) or isinstance(val, list):
        #     text_list.append(key)
        #     row_item = QtWidgets.QTreeWidgetItem([key])
        #     self.recurse_jdata(val, row_item)
        # else:
        #     text_list.append(key)
        #     text_list.append(str(val))
        #     row_item = QtWidgets.QTreeWidgetItem([key, str(val), str(val)])

        tree_widget.addChild(row_item)
        self.text_to_titem.append(text_list, row_item)

        # text_list = []

        # if isinstance(val, dict) or isinstance(val, list):
        #     text_list.append(key)
        #     row_item = QtWidgets.QTreeWidgetItem([key])
        #     self.recurse_jdata(val, row_item)
        # else:
        #     text_list.append(key)
        #     text_list.append(str(val))
        #     row_item = QtWidgets.QTreeWidgetItem([key, str(val), str(val)])

        # tree_widget.addChild(row_item)
        # self.text_to_titem.append(text_list, row_item)
    
    def load_data_by_file(self):
        data = ""
        fileName, filetype = QtWidgets.QFileDialog.getOpenFileName(self, 
            "Load File:", 
            "./",
            "Json Files (*.json);;All Files (*)")
        if fileName != '':
            try:
                with open(fileName, 'rb') as f:
                    cur_encoding = chardet.detect(f.read())['encoding']
                with open(fileName, encoding=cur_encoding) as jfile:
                    data = json.load(jfile, object_pairs_hook=collections.OrderedDict)
            except Exception as e:
                print("File Open error.")
            else:
                root_item = QtWidgets.QTreeWidgetItem(["Root"])
                self.recurse_jdata(data, root_item)
                self.tree_widget.addTopLevelItem(root_item)
            finally:
                print(fileName)
    
    def load_data_by_text(self):
        jdata, okPressed = QtWidgets.QInputDialog.getText(self, 
            "Get text",
            "json:", 
            QtWidgets.QLineEdit.Normal, 
            "")
        print(okPressed, jdata)
        if okPressed and jdata != '':
            try:
                data = json.loads(jdata, object_pairs_hook=collections.OrderedDict)
            except Exception as e:
                print("Json parse error.")
            else:
                root_item = QtWidgets.QTreeWidgetItem(["Root"])
                self.recurse_jdata(data, root_item)
                self.tree_widget.addTopLevelItem(root_item)
            finally:
                print(jdata)

class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App, self).__init__()

        self.json_view = JsonView()

        self.init_menu()

        self.setCentralWidget(self.json_view)
        self.setWindowTitle("Timer Viewer")
        self.setWindowIcon(QIcon('icon.ico'))

        self.show()

    def init_menu(self):

        self.menubar = self.menuBar()
        self.menubar.setNativeMenuBar(False)
        self.file_menu = self.menubar.addMenu('File')
        self.about_menu = self.menubar.addMenu('About')
        
        load_file_action = QtWidgets.QAction('Open File', self)
        load_file_action.setShortcut('Ctrl+O')
        load_file_action.setStatusTip('Open File')
        load_file_action.triggered.connect(self.json_view.load_data_by_file)
        
        load_input_action = QtWidgets.QAction('Input', self)
        load_input_action.setShortcut('Ctrl+I')
        load_input_action.setStatusTip('Input')
        load_input_action.triggered.connect(self.json_view.load_data_by_text)
        
        exit_action = QtWidgets.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit')
        exit_action.triggered.connect(self.close)

        self.file_menu.addAction(load_file_action)
        self.file_menu.addAction(load_input_action)
        self.file_menu.addAction(exit_action)

        about_view = QtWidgets.QAction('About', self)
        about_view.setShortcut('Ctrl+A')
        about_view.setStatusTip('About')
        about_view.triggered.connect(self.show_message)

        self.about_menu.addAction(about_view)

    def show_message(self):
            QtWidgets.QMessageBox.information(self, 
                "About", 
                "author: " + __author__ + "\n\t" + "jwx844523", 
                QtWidgets.QMessageBox.Close)


    def keyPressEvent(self, e):
        # Esc退出
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


def main():
    qt_app = QtWidgets.QApplication(sys.argv)
    app = App()
    sys.exit(qt_app.exec_())

if "__main__" == __name__:
    main()
