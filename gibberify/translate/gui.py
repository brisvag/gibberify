# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
User interface using PyQt5
"""

import sys
import math
from PyQt5.QtGui import QFontDatabase, QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QComboBox, QHBoxLayout, \
    QVBoxLayout, QWidget, QPushButton, QAction, QCheckBox, QGridLayout, QGroupBox, QLabel, \
    QTabWidget, QInputDialog, QLineEdit, QMessageBox
from PyQt5.QtCore import QSize, pyqtSignal

# local imports
from .. import utils
from .. import config
from ..generate import build
from . import gibberify, degibberify


class LangMenu(QComboBox):
    """
    drop-down menus used for language picking
    """
    def __init__(self, lang_list):
        super(LangMenu, self).__init__()
        # use given language list as possible selections
        self.addItems(lang_list)

        # configure font and size
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(15)
        self.setFont(fixedfont)


class TextBox(QTextEdit):
    """
    text input/output boxes
    """
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
    """
    button used to swap input and output languages
    """
    def __init__(self):
        super(SwitchButton, self).__init__()
        # configure icon and size
        self.setIcon(QIcon(utils.clean_path(utils.assets, 'switch.png')))
        self.setIconSize(QSize(35, 35))
        # make it togglable
        self.setCheckable(True)


class SettingsWindow(QMainWindow):
    """
    settings window: allows for user configuration of languages and other properties
    """

    settings_saved = pyqtSignal()

    def __init__(self, parent):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle('Gibberify - Settings')
        self.setWindowIcon(QIcon(utils.clean_path(utils.assets, 'gibberify.png')))
        self.conf = config.import_conf()

        self.real_langs = {'bg': 'Bulgarian',
                           'ca': 'Catalan',
                           'da': 'Danish',
                           'el': 'Greek',
                           'et': 'Estonian',
                           'fr': 'French',
                           'hu': 'Hungarian',
                           'it': 'Italian',
                           'nb': 'Norwegian-Bokmål',
                           'nn': 'Norwegian-Nynorsk',
                           'pt': 'Portuguese',
                           'ru': 'Russian',
                           'sk': 'Slovak',
                           'sr': 'Serbian',
                           'cs': 'Czech',
                           'de': 'German',
                           'en': 'English',
                           'es': 'Spanish',
                           'gl': 'Galician',
                           'hr': 'Croatian',
                           'is': 'Icelandic',
                           'lt': 'Lithuanian',
                           'lv': 'Latvian',
                           'nl': 'Dutch',
                           'pl': 'Polish',
                           'ro': 'Romanian',
                           'sl': 'Slovenian',
                           'sv': 'Swedish',
                           'uk': 'Ukrainian'}

        self.gib_options = {
            'pool': 'Pool of real languages:',
            'enrich': 'Use MORE of these letters/patterns:',
            'impoverish': 'Use LESS of these letters/patterns:',
            'remove': 'NEVER use:',
        }

        # utils layout, divided in 3 vertically (tobp, mid, bot)
        lay_main = QVBoxLayout()
        container = QWidget()
        container.setLayout(lay_main)
        self.setCentralWidget(container)
        lay_top = QHBoxLayout()
        lay_main.addLayout(lay_top)
        lay_mid = QHBoxLayout()
        lay_main.addLayout(lay_mid)
        lay_bot = QHBoxLayout()
        lay_main.addLayout(lay_bot)

        # real languages selection. Vertical layout: description, languages grid
        group_real = QGroupBox('Real Languages')
        group_real_lay = QVBoxLayout()
        group_real.setLayout(group_real_lay)
        lay_top.addWidget(group_real)
        group_real_desc = (
            'Choose the pool of languages you want to be able to translate from '
            'and/or use for the generation of gibberish languages. '
            'Languages that are used by some gibberish language will be added automatically upon saving.'
        )
        group_real_desc_label = QLabel(group_real_desc)
        group_real_desc_label.setWordWrap(True)
        group_real_lay.addWidget(group_real_desc_label)

        # grid layout of language checkboxes
        real_langs_lay = QGridLayout()
        real_langs_widg = QWidget()
        real_langs_widg.setLayout(real_langs_lay)
        group_real_lay.addWidget(real_langs_widg)
        columns = 5     # arbitrary number TODO: would be nice to have it dynamically adjusted
        rows = math.ceil(len(self.real_langs) / columns)
        langs = self.real_langs
        # save them for later access
        self.real_lang_widgets = {}
        for i in range(rows):
            for j in range(columns):
                # create a box
                sub_layout = QHBoxLayout()
                lang = langs.popitem()
                cb = QCheckBox(f'{lang[1]} ({lang[0]})', self)
                cb.setObjectName(lang[0])
                # store it in dictionary for usage later
                self.real_lang_widgets[lang[0]] = cb
                # add it to the sub_layout
                sub_layout.addWidget(cb)
                real_langs_lay.addLayout(sub_layout, i, j)
                if not langs:
                    break

        # gibberish languages options. Vertical layout: description, language tabs
        group_gib = QGroupBox('Gibberish Languages')
        group_gib_lay = QVBoxLayout()
        group_gib.setLayout(group_gib_lay)
        lay_mid.addWidget(group_gib)
        group_gib_desc = (
            'Choose your custom options for the generation of gibberish languages.\n'
            'To add a new language, press the plus on the right and come up with a three-letter code. '
            'For each option, give a set entries. Separate them with just a space (e.g.: "it en ru").\n'
            'To delete a language, simply press the minus button.\n\n'
            'HINT: writing something multiple times has an effect! "en en it" will use twice as often '
            'syllables from the English language than from Italian. The same goes for the rest: '
            f'setting the "Use less" field to "gr gr ca" will remove more "gr"s than "ca"s from your language.'
        )
        group_gib_desc_label = QLabel(group_gib_desc)
        group_gib_desc_label.setWordWrap(True)
        group_gib_lay.addWidget(group_gib_desc_label)

        # tab widget: will create a tab for each gibberish language for customization
        self.gib_tabs = QTabWidget()
        # store them for later access
        self.gib_langs_widgets = {}
        group_gib_lay.addWidget(self.gib_tabs)

        # plus and minus buttons. Horizontally added to lay_mid
        buttons_lay = QVBoxLayout()
        lay_mid.addLayout(buttons_lay)
        big_font = QFont("Times", 20, QFont.Bold)

        # plus button
        buttons_lay.addStretch(1)
        add_lang_button = QPushButton()
        add_lang_button.setText('+')
        add_lang_button.setFont(big_font)
        add_lang_button.setFixedSize(35, 35)
        buttons_lay.addWidget(add_lang_button)
        add_lang_button.clicked.connect(self.add_gib_lang)

        # minus button
        delete_lang_button = QPushButton()
        delete_lang_button.setText('-')
        delete_lang_button.setFont(big_font)
        delete_lang_button.setFixedSize(35, 35)
        buttons_lay.addWidget(delete_lang_button)
        delete_lang_button.clicked.connect(self.delete_curr_gib_lang)
        buttons_lay.addStretch(1)

        # set options to current configuration
        self.set_current(config.import_conf())

        # ok, default and cancel buttons
        lay_bot.addStretch(1)
        ok_button = QPushButton()
        ok_button.setText('OK')
        lay_bot.addWidget(ok_button)

        default_button = QPushButton()
        default_button.setText('Default')
        lay_bot.addWidget(default_button)

        cancel_button = QPushButton()
        cancel_button.setText('Cancel')
        lay_bot.addWidget(cancel_button)
        lay_bot.addStretch(1)

        # connect buttons to functions
        ok_button.clicked.connect(self.save_settings)
        default_button.clicked.connect(self.set_defaults)
        cancel_button.clicked.connect(self.discard_and_close)

    def add_gib_lang(self, default_code=None, default_options=None):
        """
        creates a new tab for a gibberish language. If data is provided, populates it with it;
        otherwise, prompts for a new language code and creates an empty tab
        """
        new_lang = QWidget()
        tab_layout = QGridLayout()
        new_lang.setLayout(tab_layout)

        if bool(default_code) != bool(default_options):
            raise Exception('defaults must be given all, or none')

        # prompt for language code
        if not default_code:
            code, ok_pressed = QInputDialog.getText(self, 'New gibberish language',
                                                    'Three-letter code:', QLineEdit.Normal, '')
        else:
            ok_pressed = True
            code = default_code

        if ok_pressed and len(code) == 3 and code.isalpha():
            self.gib_tabs.addTab(new_lang, code.lower())
            # add to widget dictionary
            self.gib_langs_widgets[code.lower()] = new_lang

            # create option boxes
            for i, (option, desc) in enumerate(self.gib_options.items()):
                option_desc = QLabel()
                option_desc.setText(desc)
                option_box = QLineEdit()
                option_box.setObjectName(option)

                # fill in provided data, if present
                if default_options:
                    option_box.setText(' '.join(default_options[option]))

                # show widget in tabs
                tab_layout.addWidget(option_desc, i, 0)
                tab_layout.addWidget(option_box, i, 1)

    def no_confirm(self, title, question):
        """
        ask for confirmation on a question

        return True if answer is NO
        """
        confirm_box = QMessageBox()
        confirm = confirm_box.question(self, title, question,
                                       confirm_box.Yes | confirm_box.No)

        return confirm != confirm_box.Yes

    def delete_curr_gib_lang(self):
        """
        delete the currently active gibberish language tab
        """
        if self.no_confirm('Delete Language', 'Are you sure?\nThis will delete the configuration '
                                              'for the current language.'):
            return

        self.delete_gib_lang()

    def delete_gib_lang(self, widget=None):
        """
        delete a named gibberish language, regardless of active tab
        """
        # needed if we come here through set_current
        if widget:
            self.gib_tabs.setCurrentWidget(widget)

        idx = self.gib_tabs.currentIndex()
        code = self.gib_tabs.tabText(idx)
        self.gib_langs_widgets.pop(code).deleteLater()
        self.gib_tabs.removeTab(idx)

    def set_current(self, conf):
        """
        set currenty displayed settings to the provided configuration
        """
        # set real languages
        for real_lang, widget in self.real_lang_widgets.items():
            if real_lang in conf['real_langs']:
                widget.setChecked(True)
            else:
                widget.setChecked(False)
        # set gibberish languages
        for widget in list(self.gib_langs_widgets.values()):    # list creation is needed to avoid runtime error
            self.delete_gib_lang(widget)
        for gib_lang, options in conf['gib_langs'].items():
            self.add_gib_lang(gib_lang, options)

    def reset_current(self):
        """
        reset displayed settings to pre-edits configuration
        """
        if self.no_confirm('Reset previous settings', 'Are you sure to reset to the previous configuration?\n'
                                                      'You will lose all your current settings.'):
            return

        self.set_current(self.conf)

    def set_defaults(self):
        """
        set displayed settings to default configuration
        """
        if self.no_confirm('Reset to Default', 'Are you sure to reset to defaults?\n'
                                               'You will lose all your current settings.'):
            return

        conf = config.get_defaults()
        self.set_current(conf)

    def save_settings(self):
        """
        parse current configuration and save it as a config file
        """
        if self.no_confirm('Save and Exit', 'Are you sure ?\n'
                                            'You will overwrite all your previous settings.\n\n'
                                            'NOTE: IT MAY TAKE A FEW MINUTES TO GENERATE ALL THE SYLLABLES!'):
            return

        # create conf based on current state
        conf = {
            'real_langs': [],
            'gib_langs': {}
        }

        # parse active language checkboxes
        for real_lang, widget in self.real_lang_widgets.items():
            if widget.checkState():
                conf['real_langs'].append(widget.objectName())
        # parse gibberish language options and save them in dictionary
        for gib_lang, tab in self.gib_langs_widgets.items():
            conf['gib_langs'][gib_lang] = {}
            for child in tab.children():
                if isinstance(child, QLineEdit):
                    option = child.objectName()
                    values = child.text()
                    conf['gib_langs'][gib_lang][option] = values.lower().split()

        # if real languages are used for gib_langs but not ticked, add them back in
        for _, options in conf['gib_langs'].items():
            for lang in options['pool']:
                if lang not in conf['real_langs']:
                    conf['real_langs'].append(lang)

        # write output in config file
        config.write_conf(conf)
        self.conf = conf
        # rebuild dictionaries based on new config
        build()
        self.settings_saved.emit()
        self.close()

    def discard_and_close(self):
        """
        discard current changes and exit the settings window
        """
        if self.no_confirm('Discard Changes', 'Are you sure?\n'
                                              'You will discard and lose your changes.'):
            return

        self.close()


class MainWindow(QMainWindow):
    """
    main window class. Contains main translator and settings menu
    """

    ready = pyqtSignal()

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Gibberify')
        self.setWindowIcon(QIcon(utils.clean_path(utils.assets, 'gibberify.png')))
        self.conf = config.import_conf()

        # MENU
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

        # WIDGETS
        # create textboxes
        self.text_in = TextBox('Type your text here.')
        self.text_out = TextBox('Get your translation here.', readonly=True)
        # create language drop-down menus
        self.lang_in_box = LangMenu(self.conf['real_langs'])
        self.lang_out_box = LangMenu([lang for lang in self.conf['gib_langs']])
        # create switch button
        self.switch = SwitchButton()

        # INITIALIZATION
        # and initialize languages to current settings
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

        # update languages when combobox are modified
        self.lang_in_box.currentTextChanged.connect(self.update_languages)
        self.lang_out_box.currentTextChanged.connect(self.update_languages)

        # swap languages when button is toggled
        self.switch.clicked.connect(self.swap)

        # run gibberify each time something changes
        self.text_in.textChanged.connect(self.translate)
        self.ready.connect(self.translate)
        self.show()

    def init_conf(self):
        """
        initialize transalor to currently loaded configuration
        """
        self.conf = config.import_conf()
        # keep signals from firing to prevent crashes
        self.lang_in_box.blockSignals(True)
        self.lang_out_box.blockSignals(True)

        self.lang_in_box.clear()
        self.lang_out_box.clear()
        self.lang_in_box.addItems(self.conf['real_langs'])
        self.lang_out_box.addItems([lang for lang in self.conf['gib_langs']])

        self.lang_in_box.blockSignals(False)
        self.lang_out_box.blockSignals(False)
        self.update_languages()

    def is_ready(self):
        """
        message other functions that translator is ready to translate
        """
        self.ready.emit()

    def translate(self):
        """
        run gibberify on current text_in
        """
        textin = self.text_in.toPlainText()
        # set new text_out as translation
        if not self.switch.isChecked():
            self.text_out.setText(gibberify(self.translator, textin))
        else:
            self.text_out.setText(degibberify(self.translator, textin))

    def update_languages(self):
        """
        update languages based on drop-down menus
        """
        self.lang_in = self.lang_in_box.currentText()
        self.lang_out = self.lang_out_box.currentText()
        self.is_ready()

    def update_translator(self):
        """
        update translator to currently selected languages
        """
        self.translator = utils.access_data('dicts', self.lang_in, self.lang_out)

    def swap(self):
        """
        swap input/output. Keep current languages and texts and swap those too.
        """
        # keep signals from firing to prevent crashes
        self.lang_in_box.blockSignals(True)
        self.lang_out_box.blockSignals(True)

        # save some variables and clear boxes
        curr_lang_in = self.lang_in_box.currentText()
        curr_lang_out = self.lang_out_box.currentText()
        curr_text_out = self.text_out.toPlainText()
        self.lang_in_box.clear()
        self.lang_out_box.clear()

        if self.switch.isChecked():
            self.switch.setStyleSheet("background-color: red")
            # switch around language boxes
            self.lang_in_box.addItems([lang for lang in self.conf['gib_langs']])
            self.lang_out_box.addItems(self.conf['real_langs'])
        else:
            self.switch.setStyleSheet("background-color: white")
            # switch around language boxes
            self.lang_in_box.addItems(self.conf['real_langs'])
            self.lang_out_box.addItems([lang for lang in self.conf['gib_langs']])

        # re-insert old text_out in text_in
        self.text_in.setText(curr_text_out)
        # re-set old languages, but inverted
        self.lang_in_box.setCurrentText(curr_lang_out)
        self.lang_out_box.setCurrentText(curr_lang_in)

        self.lang_in_box.blockSignals(False)
        self.lang_out_box.blockSignals(False)
        self.update_languages()

    def open_settings(self):
        """
        open settings window. Initialize configuration to new settings if received save signal
        """
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()
        # update config after saving settings
        self.settings_window.settings_saved.connect(self.init_conf)


def gui():
    """
    launch GUI version of Gibberify
    """
    app = QApplication(sys.argv)
    app.setApplicationName('Gibberify')

    window = MainWindow()

    try:
        app.exec_()
    except KeyboardInterrupt:
        pass
