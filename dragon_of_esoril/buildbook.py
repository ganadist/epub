#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob, sys

OUTNAME ='dragon_of_esoril'

basename = os.path.dirname(__file__) or '.'
epub_path = os.path.sep.join((basename, '..', 'epub')) 
sys.path.append(epub_path)

import ez_epub
import epub
import parse, source

source.fetch()

book = ez_epub.Book()
book.lang = 'ko-KR'
book.title = '에소릴의 드래곤'
book.authors = ['이영도',]
sections = []

paragraph = []
pattern = os.path.sep.join((basename, 'source', '*'))
for filename in sorted(glob.glob(pattern)):
	for line in parse.get_paragraph(filename):
		paragraph.append((line.text.replace('&lt;', '<').replace('&gt;', '>') or '', ''))
		paragraph.append(('\n', ''))

section = ez_epub.Section()
section.text = paragraph
book.sections = [section,]
book.make(OUTNAME)

