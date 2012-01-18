#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob, sys
from multiprocessing import Pool

basename = os.path.dirname(__file__) or '.'
epub_path = os.path.sep.join((basename, '..', 'epub')) 
sys.path.append(epub_path)

import ez_epub
import epub
import parse

def buildBook(filename):
	if not os.access(filename, os.R_OK):
		print filename, 'is not exist'
		return

	basename = os.path.basename(filename)
	WORKDIR = basename

	try:
		data = parse.getData(filename)
		TITLE, AUTHOR, SECTIONS = parse.parse(data)
	except ParseError, e:
		print 'parse error', filename, e
		return

	OUTDIR = AUTHOR.strip()

	try:
		os.makedirs(OUTDIR)
	except:
		pass

	book = ez_epub.Book()
	book.lang = 'ko-KR'
	book.title = TITLE
	book.cover = os.path.splitext(filename)[0] + '.jpg'
	book.authors = [AUTHOR,]

	book.sections = SECTIONS
	book.make(WORKDIR)


	OUTNAME = os.path.sep.join(
			(OUTDIR, TITLE.replace('/', '／') + '.epub'))
	print 'write', OUTNAME, 'from', filename

	epub.EpubBook.createArchive(WORKDIR, OUTNAME)


	os.system('rm -rf ' + WORKDIR + " " + WORKDIR + '.epub')

from xml.etree.ElementTree import ParseError

pool = Pool(os.sysconf("SC_NPROCESSORS_ONLN"))

pool.map(buildBook, sys.argv[1:])

