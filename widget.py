import sys
import json

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QRadioButton, QButtonGroup, QCheckBox
from PySide6.QtCore import Qt
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

        line_layout = QHBoxLayout()
        self.edit = QLineEdit(self)
        line_layout.addWidget(self.edit)
        go = QPushButton("GO!", self)
        line_layout.addWidget(go)

        main_layout.addLayout(line_layout)

        self.label = QLabel(self)
        main_layout.addWidget(self.label)

        go.clicked.connect(self.onGo)
        self.edit.returnPressed.connect(self.onGo)
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)        

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

        self.clipboard = QCheckBox("Copy result to the clipboard", self)
        if self.config["copy"]:
            self.clipboard.setCheckState(Qt.CheckState.Checked)
        self.clipboard.clicked.connect(self.onClipboard)

        main_layout.addWidget(self.clipboard)

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

        self.save = QPushButton("Save settings", self)
        self.save.setEnabled(False)
        self.save.clicked.connect(self.onSave)

        main_layout.addWidget(self.save)

    def onGo(self):
        text = self.edit.text()

        name = self.converter.convert(text, self.config["hyphen_options"])
        self.label.setText(name)
        if self.config["copy"]:
            cb = QClipboard()
            cb.setText(name)

    def onLanguage(self, id):
        self.config["language"] = self.config["valid_languages"][id]["code"]

        self.converter.setup(self.config["language"], self.config["filename"])
        self.onGo()

        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onClipboard(self):
        if self.clipboard.checkState() == Qt.CheckState.Checked:
            self.config["copy"] = True
        else:
            self.config["copy"] = False

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

        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onOneWord(self):
        if self.oneword.checkState() == Qt.CheckState.Checked:
            self.config["hyphen_options"]["one_word"] = False
        else:
            self.config["hyphen_options"]["one_word"] = True

        if not self.dirty:
            self.dirty = True
            self.save.setEnabled(True)

    def onSave(self):
        if not self.dirty:
            self.save.setEnabled(False)
            return
        
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=4)

        self.dirty = False
        self.save.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
