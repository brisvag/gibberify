# Gibberish? It's MUSIC to my ears!

Or, as an Orc might say:

"**Sausdrospo? Jl'gras GUSSFORT bav elf gib!**"

Gibberify is a simple gibberish generator that translates words from a real language to an (almost) pronounceable gibberish.

# Installation

If you have python (3.6+) installed:
```bash
pip install --user git+git://github.com/brisvag/gibberify.git#egg=gibberify
```

Pip should automatically add the script to your `PATH`, so you can simply run `gibberify` from the command line.

## What is this `pip` you are talking about? I wanna make gibberish!

No worries! For ease of use, there is also a standalone executable version of Gibberify, that you can find
[**here**](https://github.com/brisvag/gibberify/releases/latest), under "_Assets_".
Download the latest release for your operative system, unzip it and double-click the shit out of it. 

    The standalone was generated with PyInstaller using the configuration file `gibberify.spec`.
    If you want to generate it yourself, just run `pyinstaller gibberify.spec` from the main
    directory (you will need pyinstaller installed).

# Usage

To open the graphical interface, simply run:
```
gibberify
```
(or just double click on the executable).

**DISCLAIMER**: the reverse translation function is experimental and, frankly, terrible. Don't expect much from it.

You can also translate from the command line. To print the help, run:
```
gibberify -h
```

# Customisation

To change settings in the GUI, go click on `edit` and then `settings`.

**WARNING: EXPECT THE PROGRAM TO FREEZE FOR A FEW SECONDS AFTER SAVING!**

Several options are available to tune the gibberish language generation:
- `pool`: pool of real languages to use as a starting point for syllable generation
- `enrich`: letters (or patterns) that you want to have a lot of
- `impoverish`: letters (or patterns) that you want to have few of
- `remove`: letters (or patterns) that you want NONE of

The following is an example config for orcish:
```
"orc": {
  "pool": ["ru", "de"],
  "enrich": ["g", "k", "r"],
  "impoverish": ["w"],
  "remove": []
}
```
This config results in a language based on Russian and German in which `g`, `k` and `r` appear often and
`w` appears rarely. You can also use patterns (such as `mom`) instead of single letters and specify the same thing
more than once (such as `["g", "g", "g"]`) to enrich/impoverish even more.

# Troubleshooting

### Issue with PyQt5-sip import
```bash
pip install --user --upgrade PyQt5
pip install --user --upgrade PyQt5-sip
```

### If you used previous versions of the program...
... and now get strange errors, it might be caused by changes in the core file structures
from older versions. To remove all the old files and start anew, try running:
```bash
gibberify --uninstall
```
If this doesn't fix it, come back here and open an issue, copy-pasting the error message.

# Advanced and additional info
To edit the configuration from the command line:
```bash
gibberify --config
```
Be careful not to screw up the `json` format!

If anything goes wrong, gibberify will open the config file to let you try and fix it. If that fails too, it will revert
to defaults and save a backup of your broken configuration.

If you just changed some settings for the gibberish languages, you can simply re-build only the translation dictionaries:
```bash
gibberify --rebuild-dicts
```

Syllables are generated (and later matched) using hyphenation rules from several languages at the same time for a few reasons:
- generate reasonable outcome, in contrast to (for example) English alone. `wardrobe` and `nightstand` contain only one syllable? For real?
- be more consistent, producing a more useful set of syllables that contain fewer weird strings that appear only once in the whole language.
  This is particularly useful for _reverse translations_.

Right now the gibberish dictionaries I'm "shipping" have settings that I arbitrarily decided. They sound much better now that
they used to, but please, try out some stuff yourself and let me know if you find anything better!

# This line of code sucks! AKA: Contributing
Do you want to change it? Feel free to fork and PR! For testing, you can also import `gibberify` as a module
(_this is now much easier and better!_):
```python3
import gibberify

# anything configuration related
conf = gibberify.Config()
conf.edit()
conf.write()

# build dictionaries based on the config
gibberify.build(conf)

# translate something
tr = gibberify.Translator('en', 'orc')
# just call it to run a translation
tr('I love ALE!')
# you can change attributes, and the translation updates accordingly
tr.text_in = 'This is a new text!'
tr.lang_out = 'gob'
tr()
```

---

# RESOURCES

Gibberify uses words taken from a streamlined version of
[wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries)
(forked [here](https://github.com/brisvag/dictionaries)) to generate new syllables, 
which are then used to convert real language into a wrangled mess of nonsense.

A pre-generated collection of syllables is hosted on [gibberify-data](https://github.com/brisvag/gibberify-data),
to expedite the installation. However, you're free to generate the syllables yourself from scratch by downloading the aforementioned
words with `--force-download`.

_Icons made by_
- _[Freepik](https://www.freepik.com/) from [Flaticon](https://www.flaticon.com/)_
- _[Good Ware](https://www.flaticon.com/authors/good-ware) from [Flaticon](https://www.flaticon.com/)_
