import sys
import json

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QRadioButton, QButtonGroup, QCheckBox, QFileDialog
from PySide6.QtCore import Qt, QDir
from PySide6.QtGui import QClipboard

from pinyin_converter import PinyinConverter

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.dirty = False

        self.setWindowTitle("Pinyin converter")

        self.config = json.load(open("config.json"))
        self.converter = PinyinConverter(self.config["language"], self.config["filename"])

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # main editLine, go button and result label
        line_layout = QHBoxLayout()
        self.edit = QLineEdit(self)
        line_layout.addWidget(self.edit)
        go = QPushButton("GO!", self)
        line_layout.addWidget(go)

        main_layout.addLayout(line_layout)

        self.label = QLabel(self)
        main_layout.addWidget(self.label)

        # button can be clicked or return can be pressed inside the lineEdit
        # the label can be selectable for manual clipboard feature, if the auto clipboard feature is disabled
        go.clicked.connect(self.onGo)
        self.edit.returnPressed.connect(self.onGo)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)        

        # language setting controls
        langLayout = QHBoxLayout()
        languageGroup = QButtonGroup(self)
        for i in range(0, len(self.config["valid_languages"])):
            lang = self.config["valid_languages"][i]
            radio = QRadioButton(lang["code"])
            radio.setToolTip(lang["name"])
            langLayout.addWidget(radio)
            languageGroup.addButton(radio, i)
            if lang["code"] == self.config["language"]:
                radio.setChecked(True)        
        
        languageGroup.idClicked.connect(self.onLanguage)

        main_layout.addLayout(langLayout)

        # clipboard setting control
        self.clipboard = QCheckBox("Copy result to the clipboard", self)
        if self.config["copy"]:
            self.clipboard.setCheckState(Qt.CheckState.Checked)
        self.clipboard.clicked.connect(self.onClipboard)

        main_layout.addWidget(self.clipboard)

        # hyphen setting controls
        hyphen_layout = QHBoxLayout()
        self.hyphen = QCheckBox("Add hyphen to last names", self)
        self.oneword = QCheckBox("Only last part", self)
        if self.config["hyphen_options"]["use_hyphen"]:
            self.hyphen.setCheckState(Qt.CheckState.Checked)
        else:
            self.oneword.setEnabled(False)
        if not self.config["hyphen_options"]["one_word"]:
            self.oneword.setCheckState(Qt.CheckState.Checked)
        hyphen_layout.addWidget(self.hyphen)
        hyphen_layout.addWidget(self.oneword)
        self.hyphen.clicked.connect(self.onHyphen)
        self.oneword.clicked.connect(self.onOneWord)

        main_layout.addLayout(hyphen_layout)

        # data file setting controls
        filename_layout = QHBoxLayout()
        self.filename = QLabel("Data file: <i>" + self.config["filename"] + "</i>", self)
        filename_layout.addWidget(self.filename)
        browse = QPushButton("...", self)
        filename_layout.addWidget(browse)
        browse.clicked.connect(self.onBrowse)

        main_layout.addLayout(filename_layout)

        # save button for saving config, it's disabled at first
        self.save = QPushButton("Save settings", self)
        self.save.setEnabled(False)
        self.save.clicked.connect(self.onSave)

        main_layout.addWidget(self.save)

    def onGo(self):
        text = self.edit.text()

        name = self.converter.convert(text, self.config["hyphen_options"])
        self.label.setText(name)
        
        # copy the result to the clipboard if it's enabled
        if self.config["copy"]:
            cb = QClipboard()
            cb.setText(name)

    def onLanguage(self, id):
        self.config["language"] = self.config["valid_languages"][id]["code"]

        # re-set the converter and change the result
        self.converter.setup(self.config["language"], self.config["filename"])
        self.onGo()

        # enable the Save button
        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onClipboard(self):
        if self.clipboard.checkState() == Qt.CheckState.Checked:
            self.config["copy"] = True
        else:
            self.config["copy"] = False

        # enable the Save button
        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onHyphen(self):
        if self.hyphen.checkState() == Qt.CheckState.Checked:
            self.config["hyphen_options"]["use_hyphen"] = True
            self.oneword.setEnabled(True)
        else:
            self.config["hyphen_options"]["use_hyphen"] = False
            self.oneword.setEnabled(False)

        # enable the Save button
        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onOneWord(self):
        if self.oneword.checkState() == Qt.CheckState.Checked:
            self.config["hyphen_options"]["one_word"] = False
        else:
            self.config["hyphen_options"]["one_word"] = True

        # enable the Save button
        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onBrowse(self):
        filename = QFileDialog.getOpenFileName(self, "Open data file", QDir.currentPath(), "JSON files (*.json)")[0]
        if filename != "":
            # if the path is the same as the working path, we remove the directory and save only the filename itself
            fname = filename.split("/")[-1]
            dir = filename[:len(filename)-len(fname)]
            if dir == QDir.currentPath() + "/":
                filename = fname

            # set the new data file name and re-set the converter
            self.config["filename"] = filename
            self.filename.setText("Data file: <i>" + self.config["filename"] + "</i>")

            self.converter.setup(self.config["language"], self.config["filename"])

            # enable the Save button
            if not self.dirty:
                self.dirty = True
                self.save.setEnabled(True)

    def onSave(self):
        if not self.dirty:
            self.save.setEnabled(False)
            return
        
        # saving config
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

        # disable the Save button
        self.dirty = False
        self.save.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
