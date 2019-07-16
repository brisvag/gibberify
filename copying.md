Any file in this project that doesn't state otherwise, and isn't listed as an
exception below, is Copyright 2019-2019 The gibberify authors, and licensed
under the terms of the GNU General Public License Version 3, or
(at your option) any later version ("GPL3+").
A copy of the license can be found in [LICENSE](LICENSE).

_the gibberify authors_ are:

| Full name                   | aliases                     | E-Mail                                            |
|-----------------------------|-----------------------------|---------------------------------------------------|
| Lorenzo Gaifas              | brisvag                     | brisvag à gmail dawt com                          |

If you're a first-time committer, add yourself to the above list. This is not
just for legal reasons, but also to keep an overview of all those nicknames.

For some authors, the full names and/or e-mail addresses are unknown. They have
been marked by "?". Luckily, those author's contributions are only small typo
fixes, so no copyright concerns should arise from this.
If your info is missing, wrong, or you want it to be removed for whatever
reason, please contact us.

A full list of all gibberify authors ("contributors") can also be determined
from the VCS, e.g. via `git shortlog -sne`, or conveniently looked up on
[the GitHub web interface](https://github.com/martinitoolspymol/gibberify/graphs/contributors).

Details on individual authorships of files can be obtained via the VCS,
e.g. via `git blame`, or the GitHub web interface.

If you wish to include a file from gibberify in your project, make sure to
include all required legal info. The easiest way to do this would probably
be to include a copy of this file (`copying.md`), and to leave the file's
copyright header untouched.

Per-file license header guidelines:

In addition to this file, to prevent legal caveats, every source file *must*
include a header.

**gibberify-native** source files, that is, files that were created by
_the gibberify authors_, require the following one-line header, preferably in
the first line, as a comment:

    Copyright 20XX-20YY the gibberify authors. See copying.md for legal info.

`20XX` is the year when the file was created, and `20YY` is the year when the
file was last edited. When editing a file, make sure the last-modification year
is still correct.

**3rd-party** source files, that is, files that were taken from other open-
source projects, require the following, longer header:

    This file was ((taken|adapted)|contains (data|code)) from $PROJECT,
    Copyright 1337-2013 Your Mom.
    It's licensed under the terms of the 3-clause BSD license.
    < any amount of lines of further legal information required by $PROJECT,
      such as a reference to a copy of the $PROJECT's README or AUTHORS file >
    < if third-party files from more than the one project were used in this
      file, copy the above any number of times >
    (Modifications|Other (data|code)|Everything else) Copyright 20XX-20YY the gibberify authors.
    See copying.md for further legal info.

In addition to the gibberify header, the file's original license header should
be retained if in doubt.

Authors of 3rd-party files should generally not be entered in the
"gibberify authors" list.

All 3rd-party files **must** be included in the following list:

List of all 3rd-party files in gibberify:

- *None*

#### Disclaimer

Notes about this file:

I (`brisvag`) am not a lawyer. This is a free software project, we're doing this for
fun. People convinced me that this legal shit must be done, so I did it, even
though I'd rather have spent the time on useful parts of the project.
If you see any legal issues, feel free to contact me.

I, personally, despise in-sourcefile legal text blocks. They're a pest,
and unlike many others, I don't simply accept them because
"that is what everybody does". Thus, I worked out the minimal 1-line text above,
which should be free of legal caveats, and a reasonable compromise.
I'd be happy to see it used in other projects; you're free to use this file
(`copying.md`) as a template for your project's legal documentation.

------

This file was based on `copying.md` in https://github.com/SFTtech/openage.
