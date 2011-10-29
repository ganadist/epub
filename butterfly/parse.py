import BeautifulSoup

def get_paragraph(filename):
	b = BeautifulSoup.BeautifulSoup(open(filename))
	table = b.findChildren('table')[1]
	tr = table.findChildren('tr')[2]
	td = tr.findChildren('td')
	contents = td[0].contents
	def x(item):
		return isinstance(item, BeautifulSoup.NavigableString)
	# filter string
	contents = filter(x, contents)
	# filter '&nbsp;'
	return map(lambda x:x.replace('&nbsp;', ' '), contents)

def get_chapter(filename, isFirst = False):
	if isFirst:
		has_title, has_chapter, has_quote = True, True, True
	else:
		has_title, has_chapter, has_quote = False, False, False

	found_chapter = False
	found_quote = False

	chapter = ''
	p = []
	paragraph = get_paragraph(filename)

	if has_title:
		# find and drop title
		paragraph = paragraph[1:]

	for line in paragraph:
		if has_chapter and not found_chapter:
			# find chapter title
			if not line.strip():
				continue
			chapter = line.strip()
			found_chapter = True
			continue

		if has_quote and not found_quote:
			# find quote
			if line.strip():
				if line[2:].startswith('            '):
					p.append([(line.strip(), 'from')])
					found_quote = True
					continue
			p.append([(line.strip(), 'quote')])
			continue

		if line.strip().startswith('--------'):
			break

		p.append([(line, '')])

	return chapter, p
		
if __name__ == '__main__':
	import sys
	for i, filename in enumerate(sys.argv[1:]):
		#print '\nCR\n'.join(get_paragraph(filename))
		get_chapter(filename, i == 0)

