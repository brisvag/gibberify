"""
User interface using PyQt5
"""

import sys
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QComboBox, QHBoxLayout,\
    QVBoxLayout, QWidget

# local imports
from .config import __real_langs__, __gib_langs__
from .utils import access_data
from .gibberify import gibberify


class LangMenu(QComboBox):
    def __init__(self, lang_list):
        super(LangMenu, self).__init__()
        # use given language list as possible selections
        self.addItems(lang_list)


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


class MainWindow(QMainWindow):
    """
    main window class
    """
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Gibberify')

        # create textboxes
        self.text_in = TextBox('Type your text here.')
        self.text_out = TextBox('Get your translation here.', readonly=True)

        # create language menus
        self.lang_in_box = LangMenu(__real_langs__)
        self.lang_out_box = LangMenu([lang for lang in __gib_langs__])
        # and initialize languages to current ones
        self.lang_in = self.lang_in_box.currentText()
        self.lang_out = self.lang_out_box.currentText()
        # initialize translator
        self.translator = None
        self.update_translator()

        # set up overall layout
        # main container
        lay_main = QHBoxLayout()
        # two sides
        lay_in = QVBoxLayout()
        lay_out = QVBoxLayout()

        # insert in/out sides in the main layout
        lay_main.addLayout(lay_in)
        lay_main.addLayout(lay_out)

        # put main layout in container and set as central widget
        container = QWidget()
        container.setLayout(lay_main)
        self.setCentralWidget(container)

        # populate layout with our stuff
        lay_in.addWidget(self.lang_in_box)
        lay_in.addWidget(self.text_in)
        lay_out.addWidget(self.lang_out_box)
        lay_out.addWidget(self.text_out)

        # update languages when combobox are modified
        self.lang_in_box.currentTextChanged.connect(self.update_lang_in)
        self.lang_out_box.currentTextChanged.connect(self.update_lang_out)

        # run gibberify each time something changes
        self.text_in.textChanged.connect(self.translate)
        self.lang_in_box.currentTextChanged.connect(self.translate)
        self.lang_out_box.currentTextChanged.connect(self.translate)
        self.show()

    def update_translator(self):
        self.translator = access_data('dicts', self.lang_in, self.lang_out)

    def translate(self):
        textin = self.text_in.toPlainText()
        # set new text_out as translation
        self.text_out.setText(gibberify(self.translator, textin))

    def update_lang_in(self, value):
        self.lang_in = value

    def update_lang_out(self, value):
        self.lang_out = value


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
