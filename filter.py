#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import codecs

pat = re.compile('[ 0-9\\u0600-\\u06FF]')
shadda = re.compile('([ًٌٍَُِْ])[ّ]')

with codecs.open(sys.argv[1], 'r', encoding='utf-8') as f:
    res = f.read()
    res = ''.join(re.findall(pat, res))
    res = res[:min(len(res), 10000)] + '.'
    res = re.sub(shadda, 'ّ\\1', res)

with codecs.open(sys.argv[2], 'w', encoding='utf-8') as f:
    f.write(res)