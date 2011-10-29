#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, glob, sys

dirname = os.path.dirname(__file__) or '.'
epub_path = os.path.sep.join((dirname, '..', 'epub')) 
print epub_path
sys.path.append(epub_path)

import ez_epub
import parse, source

source.fetch()

book = ez_epub.Book()
book.lang = 'ko-KR'
book.title = '갑각 나비'
book.authors = ['오트슨',]
sections = []

for dirname in range(1, 14):
	dirname = '%02d'%dirname
	chapter = ''
	paragraph = []
	pattern = os.path.sep.join((dirname, '*'))
	for i, filename in enumerate(sorted(glob.glob(pattern))):
		name, p = parse.get_chapter(filename, i == 0)
		if i == 0:
			chapter = name
		paragraph += p
		
	section = ez_epub.Section()
	section.title = chapter
	section.text = paragraph
	section.css = """
		.quote { 
			font-style: italic; 
			padding-left: 24px;
		}
		.from {
			font-style: bold;
			text-align: left;
			margin-left: 80px;
			margin-top: 80px;
			margin-bottom: 100px;
		}
		"""
	#print section.text[:4]
	sections.append(section)

book.sections = sections
book.make('butterfly')
