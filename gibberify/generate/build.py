# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Main entry point of the dictionary generation submodule
"""

from multiprocessing import Process

# local imports
from .syllables import Syllabizer
from .dicts import Scrambler


def build(conf, from_raw=False, force_syl_rebuild=False, force_dicts_rebuild=False):
    """
    generates all data required by gibberify to work
    """
    # spawn a process for each Syllabizer
    syl_processes = []
    for real_lang in conf['real_langs']:
        s = Syllabizer(real_lang)
        p = Process(target=s.run, kwargs={'from_raw': from_raw, 'force_rebuild': force_syl_rebuild})
        syl_processes.append(p)

    # start the processes and wait for all of them to finish before proceding
    for p in syl_processes:
        p.start()
    for p in syl_processes:
        p.join()

    # spawn a process for each Scrambler
    scr_processes = []
    for real_lang in conf['real_langs']:
        for gib_lang, gib_conf in conf['gib_langs'].items():
            # TODO: add ability to detect which dicts exist and avoid redoing them
            s = Scrambler(real_lang, gib_lang, gib_conf)
            p = Process(target=s.run, kwargs={'force': force_dicts_rebuild})
            scr_processes.append(p)

    # start the processes and wait for all of them to finish before proceding
    for p in scr_processes:
        p.start()
    for p in scr_processes:
        p.join()
