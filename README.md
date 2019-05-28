# Do you like nonsense? I'LL GIVE YOU SOME NONSENSE!

Or, as an Orc might say:

"**Tlot ivol denzikorusvovden? JAIM'FURZ OZOWIR IVOL UNARHANE DENZIKORUSVOVDEN!**"

Gibbery is a simple gibberish generator that translates words from a real language to a (almost) pronounceable gibberish.

It uses words taken from [wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries) to generate new syllables which are used to convert real language into a wrangled mess or nonsense.

#### DISCLAIMER:

This thing is heavily **WIP**. This is just the first working prototype.

Does anything weird happen? Report it using an issue or fix it yourself and send a PR!

# Usage

### Translation

Just run `gibberify.py` with python3.6 or higher. You can figure out the rest ;)

# Requirements

Everything requires python3.6 or higher.

If you just want to make some gibberish or create new dictionaries you only need `pyphen`:
```
pip install pyphen
```

If you want to fiddle around with syllables you will also need (for non-latin characters):
```
pip install transliterate
```

# Customisation

#### Sillable pool

You can use the pre-generated syllable pool present in the repo, or you can generate a new one using your preferred languages by running:

Either way, you can find the code for syllable pool generation in `syllable_pools.py`.

Syllables are generated (and later matched) using Italian hyphenation rules for a few reasons:
- they generate reasonable outcome, in contrast to English (`wardrobe` and `nightstand` contain only one syllable? For real?)
- they mostly generate pronounceable syllables that contain at least a vowel
- they are consistent (again, compared to English), producing a more useful set of syllables that contain fewer weird string that appear only once in the whole language

There are probably other ways (or other languages) to do this, but Italian is my native language so either deal with it, or improve it :P

#### Translation dictionaries

Same as above, for the most part. You can generate new ones using any combination of existing languages, it's up to you.

For now, you have to manually change the code to do so (you're smart, you can figure it out).
I plan on making this thing a bit more user friendly in the future.

Right now I only included Orcish and it's generated using German and Russian, with no real reason other than "*It sounded right*".
To be honest, I don't think this combination turned out that well so try out some stuff yourself!

# Contributing

Yes, please! Just create issues, PRs, forks and have fun!

# TODO

- use multiprocessing to speedup the hot mess that `syllable_pools.py` is.
- translation mapping should be in a unique 1 to 1 fashion to avoid repetitions, not random.
- a tiny bit of user-friendliness wouldn't hurt... 
- weighted use of syllables from different languages
