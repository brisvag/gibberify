# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

# local imports
from .. import utils
from ..config import Config
from ..translate import Translator


# TODO: this needs some SERIOUS work
def interactive():
    """
    command line interactive mode. Deal with user input and call functions accordingly
    """
    conf = Config.from_json()
    # TODO: add support for reverse translation
    # Make it a sort of menu for easier usage
    level = 0
    while True:
        try:
            if level == 0:
                # welcome and usage
                print(f'Welcome to Gibberify {utils.version}! '
                      f'Follow the prompts to translate a text.\n'
                      f'To go back to the previous menu, press Ctrl+C.\n')
                level += 1
                continue

            if level == 1:
                translator = Translator()
                # language selection
                while not translator.lang_in:
                    lang_in = input(f'What language do you want to translate from? '
                                    f'Options are: {", ".join(conf["real_langs"])}.\n')
                    # check if requested input language exists
                    if lang_in not in conf['real_langs']:
                        print(f'ERROR: you first need to generate a syllable pool for "{lang_in}"!')
                    else:
                        translator.lang_in = lang_in
                        print(f'You chose "{lang_in}".')
                while not translator.lang_out:
                    lang_out = input(f'What language do you want to translate into? '
                                     f'Options are: {", ".join(conf["gib_langs"].keys())}.\n')
                    # check if requested output language exists
                    if lang_out not in conf['gib_langs'].keys():
                        print(f'ERROR: you first need to generate a dictionary for "{lang_out}"!')
                    else:
                        translator.lang_out = lang_out
                        print(f'You chose "{lang_out}".')
                level += 1
                continue

            if level == 2:
                text = input('What do you want to translate?\n')
                translator.text_in = text
                print(translator)
                continue

        except KeyboardInterrupt:
            level -= 1
            # exit the program if user tries to go back to level 0
            if level < 1:
                print('\nGood bye!\n')
                return
            print('\nGoing back...\n')
            continue

