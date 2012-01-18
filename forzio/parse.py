import sys, os, re
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

tokenmap = {
	'gt': '>',
	'lt': '<',
	'nbsp': ' ',
	'apos': "'",
	'quot': '"',
	'amp': '&',
}

def subst(matchobj):
	token = matchobj.group(0)[1:-1].lower()
	if token in tokenmap:
		return tokenmap[token]
	if token.startswith('#'):
		return unichr(int(token[1:])).encode('utf-8')
	return ' '

def getData(filename):
	p = ElementTree.parse(openFile(filename))
	r = p.getroot()
	d = r.find('Book').find('bookData')
	title = r.find('Book').find('btitle').text
	author = r.find('Book').find('bwriter').text
	return title, author, d.text

def feed(data):
	for line in data:
		line = re.sub('&(#\d+|gt|lt|apos|quot|nbsp|amp);', subst, line, flags=re.IGNORECASE)
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

def parse(data):
	title, author, text = data

	source = feed(StringIO(text))
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
	
	sections = []

	while True:
		section = parseChapter(source)
		if not section:
			break
		sections.append(section)

	return title, author, sections
