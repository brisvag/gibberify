import json
import re
import pyphen
import random


def gibberify():
    """
    translate a text into a specified gibberish language
    """
    # load translation dictionary
    with open('../data/dicts.json') as f:
        dicts = json.load(f)

    # what language to translate into
    lang_out = input(f'What language do you want to translate into? '
                     f'Options are: {", ".join(dicts.keys())}\n')
    # check if requested output language exists
    if lang_out not in dicts:
        return f'Error: you first need to generate a dictionary for "{lang_out}".'
    else:
        inp = input(f'You chose "{lang_out}". Write the sentence you want to translate:\n')

    # split words maintaining non-word characters in the right positions
    words = re.split(r'(\W+)(\w+)', inp)

    # generate translation based on syllables
    trans_list = []
    hyph = pyphen.Pyphen(lang='it')
    for w in words:
        if re.match(r'\w+', w):
            syl = hyph.inserted(w).split('-')
            # translate syllables only if they are found, otherwise return a random one
            # TODO: for now, this will also give a warning, to see how often it happens
            trans_syl = [dicts[lang_out].get(s.lower(), random.choice(list(dicts[lang_out].keys())))
                         for s in syl]
            # save word translation
            trans_w = ''.join(trans_syl)
            # let's preserve capitalisation, at least a bit
            if w[0].isupper():
                if w.isupper():
                    trans_w = trans_w.upper()
                else:
                    trans_w = trans_w.capitalize()
        else:
            # if w is not a word, just leave it as is
            trans_w = w

        trans_list.append(trans_w)

    # join everything
    trans = ''.join(trans_list)

    # remove multiple spaces due to input or unmapped syllables
    trans = re.sub(' +', ' ', trans)

    # strip ugly whitespaces and capitalise first letter.
    # TODO: this is a hack around empty syllables at the start of a sentence. It also does not
    #       capitalise words after punctuation.
    trans = trans.strip().capitalize()

    return trans


if __name__ == '__main__':
    print(gibberify())
