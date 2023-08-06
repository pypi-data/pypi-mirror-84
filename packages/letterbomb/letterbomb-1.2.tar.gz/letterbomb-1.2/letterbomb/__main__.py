#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI interface for LetterBomb."""
import argparse
import letterbomb

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--version", action="version", version=f"{letterbomb.__proj__} v"
                                                     f"{letterbomb.__version__}"
    )
    parser.add_argument("mac", help="string of Wii's MAC address")
    parser.add_argument(
        "region", choices=["U", "E", "K", "J"], help="single-letter of Wii's region"
    )
    parser.add_argument("outfile", help="filename of ZIP archive")
    parser.add_argument(
        "-b",
        "--bundle",
        action="store_true",
        help="pack the HackMii installer into archive",
    )
    parser.add_argument("-l", "--logfile", help="filepath to put log output")
    parser.add_argument(
        "-g",
        "--loglevel",
        help="minimum logging level",
        choices=letterbomb.LOGGING_DICT.keys(),
        default="info",
    )

    vargs = vars(parser.parse_args())
    LOGGING_LEVEL = letterbomb.LOGGING_DICT[vargs["loglevel"]]
    if LOGGING_LEVEL == letterbomb.logging.DEBUG:
        print(vargs)
    if vargs["logfile"]:
        LOGGING_FILE = letterbomb.pathlib.Path(vargs["logfile"]).expanduser()
    letterbomb.__main__(
        vargs["mac"], vargs["region"], vargs["bundle"], vargs["outfile"]
    )
