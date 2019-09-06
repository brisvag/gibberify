# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
User interface using PyQt5
"""

import sys
import math
from PyQt5.QtGui import QFontDatabase, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QComboBox, QHBoxLayout,\
    QVBoxLayout, QWidget, QPushButton, QAction, QCheckBox, QGridLayout
from PyQt5.QtCore import QSize, pyqtSignal

# local imports
from . import utils
from . import config
from .gibberify import gibberify
from .degibberify import degibberify


class LangMenu(QComboBox):
    def __init__(self, lang_list):
        super(LangMenu, self).__init__()
        # use given language list as possible selections
        self.addItems(lang_list)

        # configure font and size
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(15)
        self.setFont(fixedfont)


class TextBox(QTextEdit):
    def __init__(self, placeholder, readonly=False):
        super(TextBox, self).__init__()
        # configure font
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.setFont(fixedfont)

        # set default message
        self.setPlaceholderText(placeholder)

        # set readonly
        self.setReadOnly(readonly)


class SwitchButton(QPushButton):
    def __init__(self):
        super(SwitchButton, self).__init__()
        # configure icon and size
        self.setIcon(QIcon(utils.clean_path(utils.assets, 'switch.png')))
        self.setIconSize(QSize(35, 35))
        # make it togglable
        self.setCheckable(True)


class SettingsWindow(QMainWindow):
    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle('Gibberify - Settings')
        self.setWindowIcon(QIcon(utils.clean_path(utils.assets, 'gibberify.png')))
        self.conf = config.import_conf()

        lay_main = QGridLayout(self)
        container = QWidget()
        container.setLayout(lay_main)
        self.setCentralWidget(container)

        real_langs = [
            "bg", "ca", "da", "el", "eo", "et", "fa", "fr",  "fy", "gd", "he", "hu", "ie",
            "it", "ko", "lb", "ltg", "mk", "nb",  "ne", "nn", "pt", "ru", "sk", "sr", "tk",
            "tr", "vi", "br", "cs", "de", "en", "es", "eu", "fo", "fur", "ga", "gl", "hr",
            "ia", "is", "ka", "la", "lt", "lv",  "mn", "nds", "nl", "pl", "ro", "rw", "sl",
            "sv", "tlh", "uk",
        ]

        rows = math.ceil(math.sqrt(len(real_langs)))
        columns = math.floor(math.sqrt(len(real_langs)))

        langs = real_langs
        for i in range(rows):
            for j in range(columns):
                sub_layout = QHBoxLayout()
                cb = QCheckBox(langs.pop(), self)
                sub_layout.addWidget(cb)
                lay_main.addLayout(sub_layout, i, j)
                if not langs:
                    break


class MainWindow(QMainWindow):
    """
    main window class
    """

    ready = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Gibberify')
        self.setWindowIcon(QIcon(utils.clean_path(utils.assets, 'gibberify.png')))
        self.conf = config.import_conf()

        # MENU CREATION
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu('File')
        self.edit_menu = self.menu.addMenu('Edit')

        # MENU BUTTONS
        quit_button = QAction("Quit", self)
        quit_button.triggered.connect(self.close)
        self.file_menu.addAction(quit_button)
        settings_button = QAction("Settings", self)
        settings_button.triggered.connect(self.open_settings)
        self.edit_menu.addAction(settings_button)

        # quit_button = QAction(, 'Exit', self)
        # exitButton.setShortcut('Ctrl+Q')
        # exitButton.setStatusTip('Exit application')
        # exitButton.triggered.connect(self.close)
        # fileMenu.addAction(exitButton)

        # WIDGET CREATION
        # create textboxes
        self.text_in = TextBox('Type your text here.')
        self.text_out = TextBox('Get your translation here.', readonly=True)
        # create language menus
        self.lang_in_box = LangMenu(self.conf['real_langs'])
        self.lang_out_box = LangMenu([lang for lang in self.conf['gib_langs']])
        # switch button
        self.switch = SwitchButton()

        # INITIALIZATION
        # and initialize languages to current ones
        self.lang_in = self.lang_in_box.currentText()
        self.lang_out = self.lang_out_box.currentText()
        # initialize translator
        self.translator = None
        self.update_translator()
        # run an empty translation to prevent stutter at first actual translation
        self.translate()

        # LAYOUT SETUP
        # main container
        lay_main = QHBoxLayout()
        # 3 vertical stripes
        lay_in = QVBoxLayout()
        lay_cen = QVBoxLayout()
        lay_out = QVBoxLayout()
        # insert in/out sides in the main layout
        lay_main.addLayout(lay_in)
        lay_main.addLayout(lay_cen)
        lay_main.addLayout(lay_out)
        # put main layout in container and set as central widget
        container = QWidget()
        container.setLayout(lay_main)
        self.setCentralWidget(container)

        # POPULATE LAYOUT
        # input
        lay_in.addWidget(self.lang_in_box)
        lay_in.addWidget(self.text_in)
        # output
        lay_out.addWidget(self.lang_out_box)
        lay_out.addWidget(self.text_out)
        # switch
        lay_cen.addWidget(self.switch)

        # CONNECT
        # update translator whenever ready
        self.ready.connect(self.update_translator)

#        # update languages when combobox are modified
        self.lang_in_box.currentTextChanged.connect(self.update_languages)
        self.lang_out_box.currentTextChanged.connect(self.update_languages)

        # swap languages when button is toggled
        self.switch.clicked.connect(self.swap)

        # run gibberify each time something changes
        self.text_in.textChanged.connect(self.translate)
        self.ready.connect(self.translate)
        self.show()

    def is_ready(self):
        self.ready.emit()

    def translate(self):
        textin = self.text_in.toPlainText()
        # set new text_out as translation
        if not self.switch.isChecked():
            self.text_out.setText(gibberify(self.translator, textin))
        else:
            self.text_out.setText(degibberify(self.translator, textin))

    def update_languages(self):
        self.lang_in = self.lang_in_box.currentText()
        self.lang_out = self.lang_out_box.currentText()
        self.is_ready()

    def update_translator(self):
        self.translator = utils.access_data('dicts', self.lang_in, self.lang_out)

    def swap(self):
        # keep signals from firing to prevent crashes
        self.lang_in_box.blockSignals(True)
        self.lang_out_box.blockSignals(True)

        # save some variables and clear boxes
        curr_lang_in = self.lang_in_box.currentText()
        curr_lang_out = self.lang_out_box.currentText()
        curr_text_in = self.text_in.toPlainText()
        curr_text_out = self.text_out.toPlainText()
        self.lang_in_box.clear()
        self.lang_out_box.clear()

        if self.switch.isChecked():
            self.switch.setStyleSheet("background-color: red")
            # switch around language boxes
            self.lang_in_box.clear()
            self.lang_in_box.addItems([lang for lang in self.conf['gib_langs']])
            self.lang_out_box.clear()
            self.lang_out_box.addItems(self.conf['real_langs'])
            # switch around texts
            text_out = self.text_out.toPlainText()
            self.text_in.setText(text_out)
        else:
            self.switch.setStyleSheet("background-color: white")
            # switch around language boxes
            self.lang_in_box.clear()
            self.lang_in_box.addItems(self.conf['real_langs'])
            self.lang_out_box.clear()
            self.lang_out_box.addItems([lang for lang in self.conf['gib_langs']])
            # switch around texts
            text_out = self.text_out.toPlainText()
            self.text_in.setText(text_out)

        self.lang_in_box.blockSignals(False)
        self.lang_out_box.blockSignals(False)
        self.update_languages()

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        self.settings_window.parent().setWindowTitle('this is a test')


def gui():
    app = QApplication(sys.argv)
    app.setApplicationName('Gibberify')

    window = MainWindow()

    try:
        app.exec_()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    gui()
