#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A LetterBomb fork made and optimized for Python 3.

* https://gitlab.com/whoatemybutter/letterbomb

* Original: https://github.com/fail0verflow/letterbomb

*Only works for System Menu 4.3.*
"""
import hashlib
import hmac
import logging
import os
import pathlib
import struct
import zipfile
from datetime import datetime
from datetime import timedelta

__copyright__: str = "GPLv3+"
__proj__: str = "LetterBomb"
__version__: str = "1.3.1"
__author__: str = "WhoAteMyButter"
__url__: str = "https://gitlab.com/whoatemybutter/letterbomb"
__download__: str = "https://gitlab.com/whoatemybutter/letterbomb/-/archive/master/letterbomb-master.zip"

TEMPLATES: dict = {
    "U": "./included/templates/U.bin",
    "E": "./included/templates/E.bin",
    "J": "./included/templates/J.bin",
    "K": "./included/templates/K.bin",
}

LOGGING_DICT: dict = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

LOGGING_LEVEL: int = logging.DEBUG
LOGGING_FILE: [str, pathlib.Path] = ""

HERE: pathlib.PurePath = pathlib.Path(__file__).parent
BUNDLEBASE: pathlib.Path = pathlib.Path(HERE / "included/bundled/")


def __main__(
    mac: str,
    region: str,
    pack_bundle: bool,
    output_file: [str, pathlib.Path],
) -> int:
    """
    Place resulting archive, return exit code.

    :param str mac: Full string of the Wii's MAC address
    :param str region: Region of Wii, must be single letter of U,J,K,E
    :param bool pack_bundle: Pack the BootMii installer with archive
    :param str,pathlib.Path output_file: File to write archive to
    :return int: Return code, 1 for bad mac, 2 for derp mac, 0 for success
    """
    deltatime: datetime.date = datetime.utcnow() - timedelta(1)
    delta: datetime.date = deltatime - datetime(2000, 1, 1)
    timestamp: int = delta.days * 86400 + delta.seconds
    hexmac: str = "".join([chr(int(mac[i : i + 2], 16)) for i in range(0, len(mac), 2)])
    region: str = region.upper()
    umac: str = mac.upper()
    serialized_umac: str = ":".join(
        umac[i : i + 2].zfill(2) for i in range(0, len(mac), 2)
    )
    if not LOGGING_FILE:
        logging.basicConfig(filename=LOGGING_FILE, level=LOGGING_LEVEL)

    if umac == "0017AB999999":
        logging.info("If you're using Dolphin, try File→Open instead")
        logging.critical(
            f'Derp MAC "{serialized_umac}" on: {timestamp}, region: {region}, bundle: '
            f"{pack_bundle}"
        )
        return 1

    with open(pathlib.Path(HERE / "included/oui_list.txt")) as oui_file:
        oui_list: list = oui_file.read().splitlines()

    if not any(umac.startswith(i) for i in oui_list) or len(mac) != 12:
        logging.info("The exploit will only work if you enter your Wii's MAC address")
        logging.critical(
            f'Bad MAC "{serialized_umac}" on: {timestamp}, region: {region}, bundle: {pack_bundle}'
        )
        return 1

    key: hashlib.sha1 = hashlib.sha1(hexmac.encode("latin-1") + b"\x75\x79\x79")
    dig: bytes = key.digest()

    with open(pathlib.Path(HERE / TEMPLATES[region]), "rb") as bin_template:
        blob: bytearray = bytearray(bin_template.read())
    blob[0x08:0x10] = dig[:8]
    blob[0xB0:0xC4] = b"\x00" * 20
    blob[0x7C:0x80] = struct.pack(">I", timestamp)
    blob[0x80:0x8A] = b"%010d" % timestamp
    blob[0xB0:0xC4] = hmac.new(dig[8:], blob, hashlib.sha1).digest()

    path = (
        "private/wii/title/HAEA/"
        f"{dig[:4].hex().upper()}/"
        f"{dig[4:8].hex().upper()}/"
        "%04d/%02d/%02d/%02d/%02d/HABA_#1/txt/%08X.000"
        % (
            deltatime.year,
            deltatime.month - 1,
            deltatime.day,
            deltatime.hour,
            deltatime.minute,
            timestamp,
        )
    )

    with zipfile.ZipFile(pathlib.Path(output_file).expanduser(), "w") as zip_out:
        zip_out.writestr(path, blob)
        if pack_bundle:
            for name, dpath in [
                (name, pathlib.Path(BUNDLEBASE / name))
                for name in os.listdir(BUNDLEBASE)
                if not name.startswith(".")
            ]:
                zip_out.write(dpath, name)
    logging.info(
        f'LetterBombed "{mac}" on: {timestamp}, region: {region}, bundle: {pack_bundle}'
    )
    return 0
