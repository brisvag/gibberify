import json
import re
import pyphen


def gibberify(lang_out):
    """
    translate a text into the specified gibberish language
    """
    # load translation dictionary
    with open('dicts.json') as f:
        dicts = json.load(f)

    # check if requested output language exists
    if not lang_out in dicts:
        return f'Error: you first need to generate a dictionary for "{lang_out}".'
    else:
        inp = input('Write the sentence you want to translate:\n')

    # split words maintaining non-word characters in the right positions
    words = re.split('(\W+)(\w+)', inp)

    # generate translation based on syllables
    trans_list = []
    hyph = pyphen.Pyphen(lang='it')
    for w in words:
        if re.match(r'\w+', w):
            syl = hyph.inserted(w).split('-')
            # translate syllables only if they are found, otherwise return XXX TODO: return random?
            trans_syl = [dicts[lang_out].get(s.lower(), 'XXX') for s in syl]
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
    print(gibberify('orc'))
