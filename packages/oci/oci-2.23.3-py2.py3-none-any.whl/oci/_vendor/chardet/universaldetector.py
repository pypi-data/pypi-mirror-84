# coding: utf-8
# Modified Work: Copyright (c) 2018, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.
# Original Work: Copyright (c) 2018 Character Encoding Detector contributors.  https://github.com/chardet

"""
Module containing the UniversalDetector detector class, which is the primary
class a user of ``chardet`` should use.

:author: Mark Pilgrim (initial port to Python)
:author: Shy Shalom (original C code)
:author: Dan Blanchard (major refactoring for 3.0)
:author: Ian Cordasco
"""


import codecs
import logging
import re

from .charsetgroupprober import CharSetGroupProber
from .enums import InputState, LanguageFilter, ProbingState
from .escprober import EscCharSetProber
from .latin1prober import Latin1Prober
from .mbcsgroupprober import MBCSGroupProber
from .sbcsgroupprober import SBCSGroupProber


class UniversalDetector(object):
    """
    The ``UniversalDetector`` class underlies the ``chardet.detect`` function
    and coordinates all of the different charset probers.

    To get a ``dict`` containing an encoding and its confidence, you can simply
    run:

    .. code::

            u = UniversalDetector()
            u.feed(some_bytes)
            u.close()
            detected = u.result

    """

    MINIMUM_THRESHOLD = 0.20
    HIGH_BYTE_DETECTOR = re.compile(b'[\x80-\xFF]')
    ESC_DETECTOR = re.compile(b'(\033|~{)')
    WIN_BYTE_DETECTOR = re.compile(b'[\x80-\x9F]')
    ISO_WIN_MAP = {'iso-8859-1': 'Windows-1252',
                   'iso-8859-2': 'Windows-1250',
                   'iso-8859-5': 'Windows-1251',
                   'iso-8859-6': 'Windows-1256',
                   'iso-8859-7': 'Windows-1253',
                   'iso-8859-8': 'Windows-1255',
                   'iso-8859-9': 'Windows-1254',
                   'iso-8859-13': 'Windows-1257'}

    def __init__(self, lang_filter=LanguageFilter.ALL):
        self._esc_charset_prober = None
        self._charset_probers = []
        self.result = None
        self.done = None
        self._got_data = None
        self._input_state = None
        self._last_char = None
        self.lang_filter = lang_filter
        self.logger = logging.getLogger(__name__)
        self._has_win_bytes = None
        self.reset()

    def reset(self):
        """
        Reset the UniversalDetector and all of its probers back to their
        initial states.  This is called by ``__init__``, so you only need to
        call this directly in between analyses of different documents.
        """
        self.result = {'encoding': None, 'confidence': 0.0, 'language': None}
        self.done = False
        self._got_data = False
        self._has_win_bytes = False
        self._input_state = InputState.PURE_ASCII
        self._last_char = b''
        if self._esc_charset_prober:
            self._esc_charset_prober.reset()
        for prober in self._charset_probers:
            prober.reset()

    def feed(self, byte_str):
        """
        Takes a chunk of a document and feeds it through all of the relevant
        charset probers.

        After calling ``feed``, you can check the value of the ``done``
        attribute to see if you need to continue feeding the
        ``UniversalDetector`` more data, or if it has made a prediction
        (in the ``result`` attribute).

        .. note::
           You should always call ``close`` when you're done feeding in your
           document if ``done`` is not already ``True``.
        """
        if self.done:
            return

        if not len(byte_str):
            return

        if not isinstance(byte_str, bytearray):
            byte_str = bytearray(byte_str)

        # First check for known BOMs, since these are guaranteed to be correct
        if not self._got_data:
            # If the data starts with BOM, we know it is UTF
            if byte_str.startswith(codecs.BOM_UTF8):
                # EF BB BF  UTF-8 with BOM
                self.result = {'encoding': "UTF-8-SIG",
                               'confidence': 1.0,
                               'language': ''}
            elif byte_str.startswith((codecs.BOM_UTF32_LE,
                                      codecs.BOM_UTF32_BE)):
                # FF FE 00 00  UTF-32, little-endian BOM
                # 00 00 FE FF  UTF-32, big-endian BOM
                self.result = {'encoding': "UTF-32",
                               'confidence': 1.0,
                               'language': ''}
            elif byte_str.startswith(b'\xFE\xFF\x00\x00'):
                # FE FF 00 00  UCS-4, unusual octet order BOM (3412)
                self.result = {'encoding': "X-ISO-10646-UCS-4-3412",
                               'confidence': 1.0,
                               'language': ''}
            elif byte_str.startswith(b'\x00\x00\xFF\xFE'):
                # 00 00 FF FE  UCS-4, unusual octet order BOM (2143)
                self.result = {'encoding': "X-ISO-10646-UCS-4-2143",
                               'confidence': 1.0,
                               'language': ''}
            elif byte_str.startswith((codecs.BOM_LE, codecs.BOM_BE)):
                # FF FE  UTF-16, little endian BOM
                # FE FF  UTF-16, big endian BOM
                self.result = {'encoding': "UTF-16",
                               'confidence': 1.0,
                               'language': ''}

            self._got_data = True
            if self.result['encoding'] is not None:
                self.done = True
                return

        # If none of those matched and we've only see ASCII so far, check
        # for high bytes and escape sequences
        if self._input_state == InputState.PURE_ASCII:
            if self.HIGH_BYTE_DETECTOR.search(byte_str):
                self._input_state = InputState.HIGH_BYTE
            elif self._input_state == InputState.PURE_ASCII and \
                    self.ESC_DETECTOR.search(self._last_char + byte_str):
                self._input_state = InputState.ESC_ASCII

        self._last_char = byte_str[-1:]

        # If we've seen escape sequences, use the EscCharSetProber, which
        # uses a simple state machine to check for known escape sequences in
        # HZ and ISO-2022 encodings, since those are the only encodings that
        # use such sequences.
        if self._input_state == InputState.ESC_ASCII:
            if not self._esc_charset_prober:
                self._esc_charset_prober = EscCharSetProber(self.lang_filter)
            if self._esc_charset_prober.feed(byte_str) == ProbingState.FOUND_IT:
                self.result = {'encoding':
                               self._esc_charset_prober.charset_name,
                               'confidence':
                               self._esc_charset_prober.get_confidence(),
                               'language':
                               self._esc_charset_prober.language}
                self.done = True
        # If we've seen high bytes (i.e., those with values greater than 127),
        # we need to do more complicated checks using all our multi-byte and
        # single-byte probers that are left.  The single-byte probers
        # use character bigram distributions to determine the encoding, whereas
        # the multi-byte probers use a combination of character unigram and
        # bigram distributions.
        elif self._input_state == InputState.HIGH_BYTE:
            if not self._charset_probers:
                self._charset_probers = [MBCSGroupProber(self.lang_filter)]
                # If we're checking non-CJK encodings, use single-byte prober
                if self.lang_filter & LanguageFilter.NON_CJK:
                    self._charset_probers.append(SBCSGroupProber())
                self._charset_probers.append(Latin1Prober())
            for prober in self._charset_probers:
                if prober.feed(byte_str) == ProbingState.FOUND_IT:
                    self.result = {'encoding': prober.charset_name,
                                   'confidence': prober.get_confidence(),
                                   'language': prober.language}
                    self.done = True
                    break
            if self.WIN_BYTE_DETECTOR.search(byte_str):
                self._has_win_bytes = True

    def close(self):
        """
        Stop analyzing the current document and come up with a final
        prediction.

        :returns:  The ``result`` attribute, a ``dict`` with the keys
                   `encoding`, `confidence`, and `language`.
        """
        # Don't bother with checks if we're already done
        if self.done:
            return self.result
        self.done = True

        if not self._got_data:
            self.logger.debug('no data received!')

        # Default to ASCII if it is all we've seen so far
        elif self._input_state == InputState.PURE_ASCII:
            self.result = {'encoding': 'ascii',
                           'confidence': 1.0,
                           'language': ''}

        # If we have seen non-ASCII, return the best that met MINIMUM_THRESHOLD
        elif self._input_state == InputState.HIGH_BYTE:
            prober_confidence = None
            max_prober_confidence = 0.0
            max_prober = None
            for prober in self._charset_probers:
                if not prober:
                    continue
                prober_confidence = prober.get_confidence()
                if prober_confidence > max_prober_confidence:
                    max_prober_confidence = prober_confidence
                    max_prober = prober
            if max_prober and (max_prober_confidence > self.MINIMUM_THRESHOLD):
                charset_name = max_prober.charset_name
                lower_charset_name = max_prober.charset_name.lower()
                confidence = max_prober.get_confidence()
                # Use Windows encoding name instead of ISO-8859 if we saw any
                # extra Windows-specific bytes
                if lower_charset_name.startswith('iso-8859'):
                    if self._has_win_bytes:
                        charset_name = self.ISO_WIN_MAP.get(lower_charset_name,
                                                            charset_name)
                self.result = {'encoding': charset_name,
                               'confidence': confidence,
                               'language': max_prober.language}

        # Log all prober confidences if none met MINIMUM_THRESHOLD
        if self.logger.getEffectiveLevel() == logging.DEBUG:
            if self.result['encoding'] is None:
                self.logger.debug('no probers hit minimum threshold')
                for group_prober in self._charset_probers:
                    if not group_prober:
                        continue
                    if isinstance(group_prober, CharSetGroupProber):
                        for prober in group_prober.probers:
                            self.logger.debug('%s %s confidence = %s',
                                              prober.charset_name,
                                              prober.language,
                                              prober.get_confidence())
                    else:
                        self.logger.debug('%s %s confidence = %s',
                                          prober.charset_name,
                                          prober.language,
                                          prober.get_confidence())
        return self.result
