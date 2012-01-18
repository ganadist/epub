import sys, os, re
from xml.etree import ElementTree
from StringIO import StringIO

basename = os.path.dirname(__file__) or '.'
epub_path = os.path.sep.join((basename, '..', 'epub')) 
sys.path.append(epub_path)
import ez_epub

tokenmap = {
	'gt': '>',
	'lt': '<',
	'nbsp': ' ',
	'apos': "'",
	'quot': '"',
	'amp': '&',
}

PAGEBREAK = '!@#page break#@!'

def subst(matchobj):
	token = matchobj.group(0)[1:-1].lower()
	if token in tokenmap:
		return tokenmap[token]
	if token.startswith('#'):
		return unichr(int(token[1:])).encode('UTF-8')
	return ' '

def openFile(filename):
	buf = open(filename).read()
	buf = buf.replace('EUC-KR', 'UTF-8')
	buf = buf.decode('CP949').encode('UTF-8')
	buf = re.sub('&(#\d+|gt|lt|apos|quot|nbsp|amp);', subst, buf, flags=re.IGNORECASE)
	return StringIO(buf)

def getData(filename):
	p = ElementTree.parse(openFile(filename))
	r = p.getroot()
	data = r.find('Book').find('bookData').text
	title = r.find('Book').find('btitle').text
	author = r.find('Book').find('bwriter').text
	return title, author, data

def parseChapter(source):
	section = ez_epub.Section()
	p = []

	for line in source:
		if line.startswith(PAGEBREAK):
			break
		section.title = line
		break

	for line in source:
		if line.startswith(PAGEBREAK):
			break
		p += [('', line)]

	if not p:
		return
	section.text = p
	return section

def feed(data):
	for line in data:
		line = line.strip()
		if not line:
			continue
		yield line

def parse(data):
	title, author, text = data

	source = feed(StringIO(text))
	break_count = 0

	# skip head
	for line in source:
		if line.startswith(PAGEBREAK):
			break_count += 1
			if break_count == 2:
				break
			continue
	
	sections = []

	while True:
		section = parseChapter(source)
		if not section:
			break
		sections.append(section)

	return title, author, sections
