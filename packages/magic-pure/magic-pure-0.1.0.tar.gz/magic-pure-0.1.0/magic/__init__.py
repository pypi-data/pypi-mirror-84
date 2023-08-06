# -*- coding: utf-8 -*-

from typing import Any, Text, Optional, Union

__version__ = "0.1.0"  # noqa


class Lookup:
    magic2type = {
        b"%PDF-": "PDF",
        b"SQLite format 3": "SQLite 3.x database",
        b"MZ": "PE32 executable, for MS Windows",
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01": "JPEG image data, JFIF standard"
    }

    @classmethod
    def find_longest(cls, first_bytes: bytes) -> Optional[Text]:
        for n in range(len(first_bytes), 1, -1):
            prefix = first_bytes[:n]
            if prefix in cls.magic2type:
                return cls.magic2type[prefix]
        return None


def from_file(filename: Union[bytes, str], mime: bool = ...) -> Text:
    if _is_empty(filename):
        return "empty"
    with open(filename, "rb") as fp:
        first_bytes = fp.read()[:20]
    mime_type = Lookup.find_longest(first_bytes)
    print(first_bytes[:15])

    if mime_type is None:
        if _has_only_ascii(filename):
            return "ASCII text"
        return "unknown"

    # Refine
    if mime_type == "PDF":
        with open(filename, "rb") as fp:
            version = fp.read()[5:8].decode("utf8")
            mime_type = f"PDF document, version {version}"
    return mime_type


def _is_empty(filename: Union[bytes, str]) -> bool:
    with open(filename, "rb") as fp:
        data = fp.read()
    return len(data) == 0


def _has_only_ascii(filename: Union[bytes, str]) -> bool:
    try:
        with open(filename, "r") as fp:
            data = fp.read()
    except UnicodeDecodeError:
        return False
    return all(ord(char) < 128 for char in data)
