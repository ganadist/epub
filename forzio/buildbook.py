#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob, sys

basename = os.path.dirname(__file__) or '.'
epub_path = os.path.sep.join((basename, '..', 'epub')) 
sys.path.append(epub_path)

import ez_epub
import epub
import parse

def buildBook(filename):
	data = parse.getData(filename)
	TITLE, AUTHOR, SECTIONS = parse.parse(data)

	book = ez_epub.Book()
	book.lang = 'ko-KR'
	book.title = TITLE
	book.authors = [AUTHOR,]

	book.sections = SECTIONS
	basename = os.path.basename(filename)
	OUTNAME = basename
	book.make(OUTNAME)

	epub.EpubBook.createArchive(OUTNAME, OUTNAME + '.epub')

for filename in sys.argv[1:]:
	if not os.access(filename, os.R_OK):
		print filename, 'is not exist'
		break

	buildBook(filename)