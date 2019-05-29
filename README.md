# Do you like nonsense? I'LL GIVE YOU SOME NONSENSE!

Or, as an Orc might say:

"**Ova prah iso zajdeitlhio? 'CHLI MÜLEKAR PRAH KVAGREJ ZAJDEITLHIO!**"

Gibbery is a simple gibberish generator that translates words from a real language to a (almost) pronounceable gibberish.

It uses words taken from [wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries) to generate new syllables which are used to convert real language into a wrangled mess of nonsense.

#### DISCLAIMER:

This thing is heavily **WIP**. This is just the first working prototype.

Does anything weird happen? Report it using an issue or fix it yourself and send a PR!

# Usage

### Translation

Just clone the repo and run `gibberify.py` from the gibberify folder. You can figure out the rest ;)

# Requirements

Everything requires python3.6 or higher.

If you just want to make some gibberish and create new dictionaries you only need `pyphen`:
```
pip install pyphen
```

If you want to fiddle around with syllable pools you will also need (for non-latin characters):
```
pip install transliterate
```

# Customisation

Most of the things you might wanna change are located in `config.py`.

#### Sillable pool

You can use the pre-generated syllable pool present in the repo, or you can generate a new one using your preferred languages by changing the language list in `syllable_pools.py` and running it.

Syllables are generated (and later matched) using Italian hyphenation rules for a few reasons:
- they generate reasonable outcome, in contrast to English (`wardrobe` and `nightstand` contain only one syllable? For real?)
- they mostly generate pronounceable syllables that contain at least a vowel
- they are consistent (again, compared to English), producing a more useful set of syllables that contain fewer weird strings that appear only once in the whole language

There are probably other ways (or other languages) to do this, but Italian is my native language so either deal with it, or improve it :P

#### Translation dictionaries

Same as above, for the most part. You can generate new ones using any combination of existing languages, it's up to you.

Right now the ones I'm shipping are purely arbitrary, with no real reason other than "*It sounded right*".
To be honest, I don't think my combinations turned out that well, so try out some stuff yourself and let me know what sounds best!

# Contributing

Yes, please! Just create issues, PRs, forks and fiddle around with it!

# TODO

- use multiprocessing to speedup the hot mess that `syllable_pools.py` is.
- translation mapping should be in a unique 1 to 1 fashion to avoid repetitions, not random.
- a tiny bit *more* of user-friendliness wouldn't hurt... 
- weighted use of syllables from different languages

### TOTHINKABOUT
- allow asking for higher percentage of syllables containing some specific letters?
- Maybe short syllables are more common than long ones. Mapping should reflect this. Right now, translations are almost always longer and contain longer words.
