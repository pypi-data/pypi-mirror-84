# coding: utf-8
# Modified Work: Copyright (c) 2018, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.
# Original Work: Copyright (c) 2018 Character Encoding Detector contributors.  https://github.com/chardet

import logging
import re

from .enums import ProbingState


class CharSetProber(object):

    SHORTCUT_THRESHOLD = 0.95

    def __init__(self, lang_filter=None):
        self._state = None
        self.lang_filter = lang_filter
        self.logger = logging.getLogger(__name__)

    def reset(self):
        self._state = ProbingState.DETECTING

    @property
    def charset_name(self):
        return None

    def feed(self, buf):
        pass

    @property
    def state(self):
        return self._state

    def get_confidence(self):
        return 0.0

    @staticmethod
    def filter_high_byte_only(buf):
        buf = re.sub(b'([\x00-\x7F])+', b' ', buf)
        return buf

    @staticmethod
    def filter_international_words(buf):
        """
        We define three types of bytes:
        alphabet: english alphabets [a-zA-Z]
        international: international characters [\x80-\xFF]
        marker: everything else [^a-zA-Z\x80-\xFF]

        The input buffer can be thought to contain a series of words delimited
        by markers. This function works to filter all words that contain at
        least one international character. All contiguous sequences of markers
        are replaced by a single space ascii character.

        This filter applies to all scripts which do not use English characters.
        """
        filtered = bytearray()

        # This regex expression filters out only words that have at-least one
        # international character. The word may include one marker character at
        # the end.
        words = re.findall(b'[a-zA-Z]*[\x80-\xFF]+[a-zA-Z]*[^a-zA-Z\x80-\xFF]?',
                           buf)

        for word in words:
            filtered.extend(word[:-1])

            # If the last character in the word is a marker, replace it with a
            # space as markers shouldn't affect our analysis (they are used
            # similarly across all languages and may thus have similar
            # frequencies).
            last_char = word[-1:]
            if not last_char.isalpha() and last_char < b'\x80':
                last_char = b' '
            filtered.extend(last_char)

        return filtered

    @staticmethod
    def filter_with_english_letters(buf):
        """
        Returns a copy of ``buf`` that retains only the sequences of English
        alphabet and high byte characters that are not between <> characters.
        Also retains English alphabet and high byte characters immediately
        before occurrences of >.

        This filter can be applied to all scripts which contain both English
        characters and extended ASCII characters, but is currently only used by
        ``Latin1Prober``.
        """
        filtered = bytearray()
        in_tag = False
        prev = 0

        for curr in range(len(buf)):
            # Slice here to get bytes instead of an int with Python 3
            buf_char = buf[curr:curr + 1]
            # Check if we're coming out of or entering an HTML tag
            if buf_char == b'>':
                in_tag = False
            elif buf_char == b'<':
                in_tag = True

            # If current character is not extended-ASCII and not alphabetic...
            if buf_char < b'\x80' and not buf_char.isalpha():
                # ...and we're not in a tag
                if curr > prev and not in_tag:
                    # Keep everything after last non-extended-ASCII,
                    # non-alphabetic character
                    filtered.extend(buf[prev:curr])
                    # Output a space to delimit stretch we kept
                    filtered.extend(b' ')
                prev = curr + 1

        # If we're not in a tag...
        if not in_tag:
            # Keep everything after last non-extended-ASCII, non-alphabetic
            # character
            filtered.extend(buf[prev:])

        return filtered
