# Do you like nonsense? I'LL GIVE YOU SOME NONSENSE!

Or, as an Orc might say:

"**Ova prah iso zajdeitlhio? 'CHLI MÜLEKAR PRAH KVAGREJ ZAJDEITLHIO!**"

Gibberify is a simple gibberish generator that translates words from a real language to a (almost) pronounceable gibberish.

It uses words taken from [wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries) to generate new syllables which are used to convert real language into a wrangled mess of nonsense.

#### DISCLAIMER:

This thing is heavily **WIP**. This is just the first working prototype.

Does anything weird happen? Report it using an issue or fix it yourself and send a PR!

# Usage

## Translation

Just clone the repo with:
```
git clone https://github.com/brisvag/gibberify.git
cd gibberify
``` 
and then run:
```
python -m gibberify
```

You can also translate from the command line. To print the help, run:
```
python -m gibberify -h
```

Alternatively, you can use the standalone executable `standalone/gibberify` without needing python or any dependency. Wohoo!
For now, the standalone only works on **linux**.

The standalone was generated with PyInstaller using the configuration file `gibberify.spec`.
If you want to generate it yourself, just run `pyinstaller gibberify.spec` from the main directory (you will need pyinstaller installed).

PyInstaller does not work with python3.7, use python3.6!

### Examples

- Run the program with the graphical interface using the standalone:
```
./standalone/gibberify
```
(or just double click on it)

- Translate from German to Elvish the sentence "*Hans, Get ze Flammenwerfer*" from the command line:
```
python -m gibberify -fl de -l elv -m Hans, Get ze Flammenwerfer
Skel, Foë togssaé Licfoeusuasean
```

- Translate from English (default) to Dwarvish the file `README.md`, using the standalone executable:
```
./standalone/gibberify -l dwa -m README.md
***this_is_not_a_recursive_message***
```

- Translate from Russian to Orcish (default) from `stdin`:
```
echo Privetstvuju Putina! | ./standalone/gibberify -fl ru -m -
Thorsyneftlaos Pryrheeflut!
```

# Requirements

**If you use the standalone executable, it should work out of the box, no requirements!**

Otherwise, everything requires `python3.6` or higher.

If you just want to make some gibberish and create new dictionaries you only need `pyphen` and `PyQt5`:
```
pip install pyphen pyqt5
```

If you want to fiddle around with syllable pools you will also need (for non-latin characters):
```
pip install transliterate
```

# Customisation

Most of the things you might wanna change are located in `config.py`.

## Syllable pool

You can use the pre-generated syllable pool present in the repo, or you can generate a new one using your preferred languages by editing `config.py`.

To generate new pools, run `python -m gibberify.syllable_pools` from the main directory.

Syllables are generated (and later matched) using Italian hyphenation rules for a few reasons:
- they generate reasonable outcome, in contrast to English (`wardrobe` and `nightstand` contain only one syllable? For real?)
- they mostly generate pronounceable syllables that contain at least a vowel
- they are consistent (again, compared to English), producing a more useful set of syllables that contain fewer weird strings that appear only once in the whole language

There are probably other ways (or other languages) to do this, but Italian is my native language so either deal with it, or improve it :P

## Translation dictionaries

Same as above, for the most part. You can generate new ones using any combination of existing languages, it's up to you. Just run `python -m gibberify.gibberish_dicts` from the main directory.

Right now the ones I'm shipping are purely arbitrary, with no real reason other than "*It sounded right*".
To be honest, I don't think my combinations turned out that well, so try out some stuff yourself and let me know what sounds best!

# Contributing

Yes, please! Just create issues, PRs, forks and fiddle around with it!

# TODO

- make syllable and dictionary generation easier to call
- add support for non-latin fonts in input/output
- use multiprocessing to speedup the hot mess that `syllable_pools.py` is.
- translation mapping should be in a unique 1 to 1 fashion to avoid repetitions, not random.
- a tiny bit *more* of user-friendliness wouldn't hurt... 
- weighted use of syllables from different languages
- support two-way translation (and transliteration!)

# TOTHINKABOUT
- allow asking for higher percentage of syllables containing some specific letters?
- Maybe short syllables are more common than long ones. Mapping should reflect this. Right now, translations are almost always longer and contain longer words.
