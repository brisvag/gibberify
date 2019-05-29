import json
import random

# local imports
from config import real_langs, gib_langs


def gen_dict(pool_in, pool_out):
    """
    randomly links syllables from the input pool to ones in the target pool
    in order to form translation dictionaries

    returns a dict that can be used to translate each syllable in pool_in
    """
    dict = {}

    # TODO: would be nice not to have duplicate mappings, but my attempts using a while loop were
    #       unsuccessful/ridiculously expensive
    # generate new syllables until we have mapped every syllable from syllables_full
    for syl in pool_in:
        # get a random number between 0 and 2, so syllable mapping is not 1 to 1.
        # weights are arbitrary: 10% `0`, 80% `1`, 10% `2`. This way we shouldn't end up with
        # too many empty words or very long ones
        weights = [0] + [1] * 8 + [2]
        r = random.choice(weights)
        mapping = ''.join(random.sample(pool_out, r))
        dict[syl] = mapping

    return dict


def gen_dicts():
    """
    creates dictionaries for translation from an input language into several fake languages
    """
    dicts = {}

    # make dictionary generation somewhat deterministic, cause why not
    random.seed('gibberish')

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
    for lang_in in real_langs:
        dicts[lang_in] = {}
        for lang_out, syl_set in dict_pools.items():
            print(f'Creating translation dictionary "{lang_in}-{lang_out}"...')
            dicts[lang_in][lang_out] = gen_dict(syllables_full[lang_in], syl_set)

    return dicts


if __name__ == '__main__':
    dicts = gen_dicts()
    with open(f'../data/dicts.json', 'w') as outfile:
        json.dump(dicts, outfile, indent=1)
