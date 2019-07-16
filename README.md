# Gibberish? It's MUSIC to my ears!

Or, as an Orc might say:

"**Csonnigzè? Charm'stoi OFFCNI ield tyl perb!**"

Gibberify is a simple gibberish generator that translates words from a real language to an (almost) pronounceable gibberish.

It uses words taken from a streamlined version of
[wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries)
(forked [here](https://github.com/brisvag/dictionaries)) to generate new syllables, 
which are then used to convert real language into a wrangled mess of nonsense.

#### DISCLAIMER:

This thing is **WIP**. Though the program is starting to be usable, it's still in the early stages. 

Does anything weird happen? Report it using an issue or fix it yourself and send a PR!

# Set up

Installation is now easier than ever thanks to `pip`!
```bash
pip install git+git://github.com/brisvag/gibberify.git#egg=gibberify
```

Pip will automatically add the script to your `PATH`, so you can simply run `gibberify` from the command line.

## What is this `pip` you are talking about? I wanna make gibberish!

No worries! There is also an executable version of Gibberify, that you can find
[**here**](https://github.com/brisvag/gibberify/releases/latest), under "_Assets_".
Download the latest release for your operative system, unzip it and double click the shit out of it. 

    For now, the standalone only works on **linux**.
    The standalone was generated with PyInstaller using the configuration file `gibberify.spec`.
    If you want to generate it yourself, just run `pyinstaller gibberify.spec` from the main
    directory (you will need pyinstaller installed).
    PyInstaller does not work with python3.7: use python3.6!

# Usage

To open the graphical interface, simply run:
```
gibberify
```
(or just double click on the executable).

You can also translate from the command line. To print the help, run:
```
gibberify -h
```

### Examples

- Translate from German to Elvish the sentence "*Hans, Get ze Flammenwerfer*" from the command line:
```
gibberify -f de -t elv -m Hans, Get ze Flammenwerfer
Skel, Foë togssaé Licfoeusuasean
```

- Translate from English (default) to Dwarvish the file `README.md`:
```
gibberify -l dwa -m README.md
***this_is_not_a_recursive_message***
```

- Translate from Russian to Orcish (default) from `stdin`, using gibberify as a python module:
```
echo Privetstvuju Putina! | python3 -m gibberify -fl ru -m -
Thorsyneftlaos Pryrheeflut!
```


### NEW FEATURE: REVERSE TRANSLATION

You heard it well! It's a tough guessing game, and it often fails in finding the right syllable.
However, if your sentence is long enough, you can usually guess the general meaning. Try it out by simply switching
around languages (or by pressing the big central button in the GUI):
```bash
gibberify -f orc -t en -m [orcish message here] 
```

# Customisation

**Customization is now also possible with the standalone version!**

To change settings, run:
```bash
gibberify --config
```

Unfortunately, this is still far from user friendly and the GUI is still missing a way of doing this.
Be careful not to screw up the `json` format!

## Custom languages

You can use the suggested settings, or you can generate completely new dictionaries using your preferred 
settings and languages by editing `config.py`.

If it's the first time you create dictionaries, or if you changed/added new languages in the configuration file,
you will have to download any missing dictionary and re-build the syllable pools.
```bash
gibberify --rebuild-syllables
```

If you just changed some settings for the gibberish languages, you can simply re-build only the translation dictionaries:
```bash
gibberify --rebuild-dicts
```

Syllables are generated (and later matched) using hyphenation rules from several languages at the same time for a few reasons:
- generate reasonable outcome, in contrast to (for example) English alone. `wardrobe` and `nightstand` contain only one syllable? For real?
- be more consistent, producing a more useful set of syllables that contain fewer weird strings that appear only once in the whole language.
  This is particularly useful for _reverse translations_.

Right now the gibberish dictionaries I'm shipping have very random settings. I don't think they sound/look particularly good,
so please, try out some stuff yourself and let me know what sounds best!

# I really can't stand the way you wrote this specific line of code

Do you want to change it? Feel free to fork and PR! For testing, you can also import `gibberify` as a module:
```python3
import gibberify
```

# TODO

- **make customization possible in standalone mode**
- add support for non-latin fonts in input/output
- use multiprocessing to speedup the hot mess that `syllable_pools.py` is.
- weighted use of syllables from different languages

---

_Icons made by_
- _[Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/)_
- _[Good Ware](https://www.flaticon.com/authors/good-ware) from [Flaticon](https://www.flaticon.com/)_