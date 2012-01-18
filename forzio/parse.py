import sys, os
from xml.etree import ElementTree
from StringIO import StringIO

basename = os.path.dirname(__file__) or '.'
epub_path = os.path.sep.join((basename, '..', 'epub')) 
sys.path.append(epub_path)

import ez_epub

def openFile(filename):
	buf = open(filename).read()
	buf = buf.replace('EUC-KR', 'UTF-8')
	buf = buf.decode('cp949').encode('utf-8')
	return StringIO(buf)


def getData(filename):
	p = ElementTree.parse(openFile(filename))
	r = p.getroot()
	d = r.find('Book').find('bookData')
	return d.text

def feed(data):
	for line in data:
		yield line

def createSection():
	return ez_epub.Section()

def parseChapter(source):
	section = createSection()
	title = ''
	p = []
	for line in source:
		if not line.strip():
			continue
		if line.startswith('!@#page break#@!'):
			break
		if not title:
			title = line.strip()
			section.title = title
			continue
		p += [('', line.strip())]
	if not p:
		return
	section.text = p
	return section

def parse(text):
	title = ''
	author = ''

	source = StringIO(text)
	pagebreak = 0

	# parse head
	for line in source:
		if not line.strip():
			continue
		if line.startswith('!@#page break#@!'):
			pagebreak += 1
			if pagebreak == 2:
				break
			continue
		if not title:
			title = line.strip()
			continue
		if not author:
			author = line.strip()
			continue
	
	sections = []

	while True:
		section = parseChapter(source)
		if not section:
			break
		sections.append(section)

	return title, author, sections
