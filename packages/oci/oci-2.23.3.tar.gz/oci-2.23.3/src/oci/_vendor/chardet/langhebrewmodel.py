# coding: utf-8
# Modified Work: Copyright (c) 2018, 2020, Oracle and/or its affiliates.  All rights reserved.
# This software is dual-licensed to you under the Universal Permissive License (UPL) 1.0 as shown at https://oss.oracle.com/licenses/upl or Apache License 2.0 as shown at http://www.apache.org/licenses/LICENSE-2.0. You may choose either license.
# Original Work: Copyright (c) 2018 Character Encoding Detector contributors.  https://github.com/chardet

# 255: Control characters that usually does not exist in any text
# 254: Carriage/Return
# 253: symbol (punctuation) that does not belong to word
# 252: 0 - 9

# Windows-1255 language model
# Character Mapping Table:
WIN1255_CHAR_TO_ORDER_MAP = (
255,255,255,255,255,255,255,255,255,255,254,255,255,254,255,255,  # 00
255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,  # 10
253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,  # 20
252,252,252,252,252,252,252,252,252,252,253,253,253,253,253,253,  # 30
253, 69, 91, 79, 80, 92, 89, 97, 90, 68,111,112, 82, 73, 95, 85,  # 40
 78,121, 86, 71, 67,102,107, 84,114,103,115,253,253,253,253,253,  # 50
253, 50, 74, 60, 61, 42, 76, 70, 64, 53,105, 93, 56, 65, 54, 49,  # 60
 66,110, 51, 43, 44, 63, 81, 77, 98, 75,108,253,253,253,253,253,  # 70
124,202,203,204,205, 40, 58,206,207,208,209,210,211,212,213,214,
215, 83, 52, 47, 46, 72, 32, 94,216,113,217,109,218,219,220,221,
 34,116,222,118,100,223,224,117,119,104,125,225,226, 87, 99,227,
106,122,123,228, 55,229,230,101,231,232,120,233, 48, 39, 57,234,
 30, 59, 41, 88, 33, 37, 36, 31, 29, 35,235, 62, 28,236,126,237,
238, 38, 45,239,240,241,242,243,127,244,245,246,247,248,249,250,
  9,  8, 20, 16,  3,  2, 24, 14, 22,  1, 25, 15,  4, 11,  6, 23,
 12, 19, 13, 26, 18, 27, 21, 17,  7, 10,  5,251,252,128, 96,253,
)

# Model Table:
# total sequences: 100%
# first 512 sequences: 98.4004%
# first 1024 sequences: 1.5981%
# rest  sequences:      0.087%
# negative sequences:   0.0015%
HEBREW_LANG_MODEL = (
0,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,2,3,2,1,2,0,1,0,0,
3,0,3,1,0,0,1,3,2,0,1,1,2,0,2,2,2,1,1,1,1,2,1,1,1,2,0,0,2,2,0,1,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,
1,2,1,2,1,2,0,0,2,0,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,
1,2,1,3,1,1,0,0,2,0,0,0,1,0,1,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,1,2,2,1,3,
1,2,1,1,2,2,0,0,2,2,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,2,2,2,2,3,2,
1,2,1,2,2,2,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,2,3,2,2,3,2,2,2,1,2,2,2,2,
1,2,1,1,2,2,0,1,2,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,0,2,2,2,2,2,
0,2,0,2,2,2,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,0,2,2,2,
0,2,1,2,2,2,0,0,2,1,0,0,0,0,1,0,1,0,0,0,0,0,0,2,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,2,1,2,3,2,2,2,
1,2,1,2,2,2,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,1,0,
3,3,3,3,3,3,3,3,3,2,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3,3,1,0,2,0,2,
0,2,1,2,2,2,0,0,1,2,0,0,0,0,1,0,1,0,0,0,0,0,0,1,0,0,0,2,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,2,3,2,2,3,2,1,2,1,1,1,
0,1,1,1,1,1,3,0,1,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,0,1,0,0,1,0,0,0,0,
0,0,1,0,0,0,0,0,2,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,
0,2,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,2,3,3,3,2,1,2,3,3,2,3,3,3,3,2,3,2,1,2,0,2,1,2,
0,2,0,2,2,2,0,0,1,2,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,
3,3,3,3,3,3,3,3,3,2,3,3,3,1,2,2,3,3,2,3,2,3,2,2,3,1,2,2,0,2,2,2,
0,2,1,2,2,2,0,0,1,2,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,1,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,2,3,3,2,2,2,3,3,3,3,1,3,2,2,2,
0,2,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,3,3,3,2,3,2,2,2,1,2,2,0,2,2,2,2,
0,2,0,2,2,2,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,3,3,2,3,3,3,1,3,2,3,3,2,3,3,2,2,1,2,2,2,2,2,2,
0,2,1,2,1,2,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,2,3,2,3,3,2,3,3,3,3,2,3,2,3,3,3,3,3,2,2,2,2,2,2,2,1,
0,2,0,1,2,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,3,3,3,2,1,2,3,3,3,3,3,3,3,2,3,2,3,2,1,2,3,0,2,1,2,2,
0,2,1,1,2,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,2,0,
3,3,3,3,3,3,3,3,3,2,3,3,3,3,2,1,3,1,2,2,2,1,2,3,3,1,2,1,2,2,2,2,
0,1,1,1,1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,2,0,0,0,0,0,0,0,0,
3,3,3,3,3,3,3,3,3,3,0,2,3,3,3,1,3,3,3,1,2,2,2,2,1,1,2,2,2,2,2,2,
0,2,0,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,
3,3,3,3,3,3,2,3,3,3,2,2,3,3,3,2,1,2,3,2,3,2,2,2,2,1,2,1,1,1,2,2,
0,2,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
3,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,1,0,0,0,0,0,
1,0,1,0,0,0,0,0,2,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
3,3,3,3,3,2,3,3,2,3,1,2,2,2,2,3,2,3,1,1,2,2,1,2,2,1,1,0,2,2,2,2,
0,1,0,1,2,2,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,
3,0,0,1,1,0,1,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,0,
0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
3,0,1,0,1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
3,0,0,0,1,1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,
3,2,2,1,2,2,2,2,2,2,2,1,2,2,1,2,2,1,1,1,1,1,1,1,1,2,1,1,0,3,3,3,
0,3,0,2,2,2,2,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
2,2,2,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,2,1,2,2,2,1,1,1,2,0,1,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,0,2,2,0,0,0,0,0,0,
0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,3,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,0,2,1,0,
0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
3,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,
0,3,1,1,2,2,2,2,2,1,2,2,2,1,1,2,2,2,2,2,2,2,1,2,2,1,0,1,1,1,1,0,
0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
3,2,1,1,1,1,2,1,1,2,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,
0,0,2,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,1,0,0,
2,1,1,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,2,2,1,2,1,2,1,1,1,1,0,0,0,0,
0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,2,1,2,2,2,2,2,2,2,2,2,2,1,2,1,2,1,1,2,1,1,1,2,1,2,1,2,0,1,0,1,
0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,3,1,2,2,2,1,2,2,2,2,2,2,2,2,1,2,1,1,1,1,1,1,2,1,2,1,1,0,1,0,1,
0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,1,2,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,
0,2,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,
3,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,1,1,1,1,1,1,1,0,1,1,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,2,0,1,1,1,0,1,0,0,0,1,1,0,1,1,0,0,0,0,0,1,1,0,0,
0,1,1,1,2,1,2,2,2,0,2,0,2,0,1,1,2,1,1,1,1,2,1,0,1,1,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,0,1,0,0,0,0,0,1,0,1,2,2,0,1,0,0,1,1,2,2,1,2,0,2,0,0,0,1,2,0,1,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,2,0,2,1,2,0,2,0,0,1,1,1,1,1,1,0,1,0,0,0,1,0,0,1,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,1,0,0,0,0,0,1,0,2,1,1,0,1,0,0,1,1,1,2,2,0,0,1,0,0,0,1,0,0,1,
1,1,2,1,0,1,1,1,0,1,0,1,1,1,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,2,2,1,
0,2,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,1,0,0,1,0,1,1,1,1,0,0,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,1,1,1,1,1,1,1,1,2,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,1,0,1,1,0,1,0,0,0,1,1,0,1,
2,0,1,0,1,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,0,0,1,1,2,1,1,2,0,1,0,0,0,1,1,0,1,
1,0,0,1,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,1,1,2,0,1,0,0,0,0,2,1,1,2,0,2,0,0,0,1,1,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,2,1,1,0,1,0,0,2,2,1,2,1,1,0,1,0,0,0,1,1,0,1,
2,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,1,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,1,2,2,0,0,0,0,2,1,1,1,0,2,1,1,0,0,0,2,1,0,1,
1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,1,1,2,0,1,0,0,1,1,0,2,1,1,0,1,0,0,0,1,1,0,1,
2,2,1,1,1,0,1,1,0,1,1,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,2,1,1,0,1,0,0,1,1,0,1,2,1,0,2,0,0,0,1,1,0,1,
2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,
0,1,0,0,2,0,2,1,1,0,1,0,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,1,0,1,1,2,0,1,0,0,1,1,1,0,1,0,0,1,0,0,0,1,0,0,1,
1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,0,0,0,0,0,0,0,1,0,1,1,0,0,1,0,0,2,1,1,1,1,1,0,1,0,0,0,0,1,0,1,
0,1,1,1,2,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,1,1,0,0,
)

Win1255HebrewModel = {
  'char_to_order_map': WIN1255_CHAR_TO_ORDER_MAP,
  'precedence_matrix': HEBREW_LANG_MODEL,
  'typical_positive_ratio': 0.984004,
  'keep_english_letter': False,
  'charset_name': "windows-1255",
  'language': 'Hebrew',
}
