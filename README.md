# Gibberish? It's MUSIC to my ears!

Or, as an Orc might say:

"**Strecgunssjakstrog? Nev'berg HORTPRIZ hrom strak sang!**"

Gibberify is a simple gibberish generator that translates words from a real language to an (almost) pronounceable gibberish.

It uses words taken from a streamlined version of
[wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries)
(forked [here](https://github.com/brisvag/dictionaries)) to generate new syllables, 
which are then used to convert real language into a wrangled mess of nonsense.

#### DISCLAIMER:

This thing is **WIP**. Though the program is starting to be usable, it's still in the early stages. 

Does anything weird happen? Report it using the issue tracker or fix it yourself and send a PR!

# Set up

Installation is now easier than ever thanks to `pip`!
```bash
pip install git+git://github.com/brisvag/gibberify.git#egg=gibberify
```

Pip will automatically add the script to your `PATH`, so you can simply run `gibberify` from the command line.

## What is this `pip` you are talking about? I wanna make gibberish!

No worries! There is also an executable version of Gibberify, that you can find
[**here**](https://github.com/brisvag/gibberify/releases/latest), under "_Assets_".
Download the latest release for your operative system, unzip it and double-click the shit out of it. 

    The standalone was generated with PyInstaller using the configuration file `gibberify.spec`.
    If you want to generate it yourself, just run `pyinstaller gibberify.spec` from the main
    directory (you will need pyinstaller installed).
    PyInstaller does not work with python3.7 yet: use python3.6!

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
See the **Examples** section for other command line stuff.

### NEW FEATURE: REVERSE TRANSLATION

You heard it well! It's a tough guessing game, and it often fails in finding the right syllable.
However, if your sentence is long enough, you can usually guess the general meaning. Try it out by simply switching
around languages (or by pressing the big central button in the GUI):
```bash
gibberify -f orc -t en -m [orcish message here] 
```

# Customisation

**Customization is now also possible with the standalone version AND from the GUI!**

To change settings, go click on `edit` and then `settings`.

**WARNING: EXPECT THE PROGRAM TO FREEZE FOR A COUPLE OF MINUTES AFTER SAVING! It's a lot of processing.**

Several options are available to tune the gibberish language generation:
- `pool`: pool of real languages to use as a starting point for syllable generation
- `enrich`: letters (or patterns) that you want to have a lot of
- `impoverish`: letters (or patterns) that you want to have few of
- `remove`: letters (or patterns) that you want NONE of

The following is an example config for orcish (which is the default one):
```json
"orc": {
  "pool": ["ru", "de"],
  "enrich": ["g", "k", "r"],
  "impoverish": ["w"],
  "remove": [""]
```
This config results in a language based on Russian and German in which `g`, `k` and `r` appear often and
`w` appears rarely. You can also use patterns (such as `mom`) instead of single letters and specify the same thing
more than once (such as `["g", "g", "g"]`) to enrich/impoverish even more.

# Advanced
From the command line:
```bash
gibberify --config
```
Be careful not to screw up the `json` format!

If anything goes wrong, gibberify will open the config file to let you try and fix it. If that fails too, it will revert
to defaults and save a backup of your broken configuration.

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

Do you want to change it? Feel free to fork and PR! For testing, you can also import `gibberify` as a module
(not very useful for now, but possible):
```python3
import gibberify
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

# TODO

- add support for non-latin fonts in input/output
- use multiprocessing to speedup the hot mess that `syllable_pools.py` is.

---

_Icons made by_
- _[Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/)_
- _[Good Ware](https://www.flaticon.com/authors/good-ware) from [Flaticon](https://www.flaticon.com/)_