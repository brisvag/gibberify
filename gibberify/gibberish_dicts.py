import json
import random


def gen_dicts(lang_in):
    """
    reads from an existing syllables.json file and randomly links
    syllables from the input language to the others in order to
    form translation dictionaries

    returns a dict that can be used to translate from lang_in
    to every gibberish language and viceversa
    """
    dicts = {}

    # gibberish languages and the respective template languages
    gib_langs = {
        'orc': ['ru', 'de'],
        'elv': ['fr', 'en'],
        'dwa': ['it', 'de'],
    }

    # make dictionary generation somewhat deterministic, cause why not
    random.seed('total gibberish')

    with open('../data/syllables_full.json') as f:
        syllables_full = json.load(f)

    with open('../data/syllables.json') as f:
        syllables = json.load(f)

    # create pools of syllables from template languages
    dict_pools = {}
    for l, t_list in gib_langs.items():
        # smash together template language sets
        syl_set = set()
        for t_lang in t_list:
            syl_set.update(syllables[t_lang])
        dict_pools[l] = syl_set

    # create actual translation dictionaries
    # TODO: would be nice not to have duplicate mappings, but my attempts using a while loop were
    #       unsuccessful/ridiculously expensive
    for l, syl_set in dict_pools.items():
        print(f'Creating syllable pool for "{l}"...')
        dicts[l] = {}
        # generate new syllables until we have mapped every syllable from syllables_full
        for syl in syllables_full[lang_in]:
            # get a random number between 0 and 2, so syllable mapping is not 1 to 1.
            # weights are arbitrary: 10% `0`, 80% `1`, 10% `2`. This way we shouldn.t end up with
            # too many empty words or very long ones
            weights = [0] + [1] * 8 + [2]
            r = random.choice(weights)
            mapping = ''.join(random.sample(syl_set, r))
            dicts[l][syl] = mapping

    return dicts


if __name__ == '__main__':
    dicts = gen_dicts('en')
    with open('../data/dicts.json', 'w') as outfile:
        json.dump(dicts, outfile, indent=1)
