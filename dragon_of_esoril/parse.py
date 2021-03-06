from bs4 import BeautifulSoup, Tag

def get_paragraph(filename):
	b = BeautifulSoup(open(filename))
	contents = b.findChild(attrs={'name':'navercast_div'})
	def x(item):
		return isinstance(item, Tag)
	# filter string
	contents = filter(x, contents)
	return contents

if __name__ == '__main__':
	import sys
	for i, filename in enumerate(sys.argv[1:]):
		print get_paragraph(filename)

