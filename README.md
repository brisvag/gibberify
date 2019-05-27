# INSERT_GIBBERISH_HERE

Gibbery is a simple gibberish generator that translates words from a real language to a pronounceable gibberish.

It uses words taken from [wooorm/dictionaries](https://github.com/wooorm/dictionaries/tree/master/dictionaries).

# Usage

TODO

### Sillable pool generation

You can use the pre-generated syllable pool present in the repo, or you can generate a new one using your preferred languages.

Either way, you can find the code for syllable pool generation in syllable_pools.py

Syllables are generated using Italian hyphenation rules for a few reasons:
- they generate reasonable outcome, in contrast to English (`wardrobe` is one syllable? For real?)
- they mostly generate pronounceable syllables
- they are consistent (again, compared to English), producing a more useful set of syllables that contain fewer weird string that appear only once in the whole language

There are probably other ways (or other languages) to do this, but Italian is my native language so that was my first choice.

### TODO

- use multiprocessing to speedup syllable pool generation
