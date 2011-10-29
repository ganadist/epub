BASEURL="http://drwk.com/pimangboard/read.php?code=serial&sidx=1000024"

SOURCES=[
	# chapter struct
	# (
	#	(id1, has_title, has_chapter, has_quote),
	#	(id2, has_title, has_chapter, has_quote),
	# ),
	#
	#
	(
		# chapter 1
		("122982", True, True, True,),
		("122983", False, False, False, ),
	),
	(
		# chapter 2
		("122984", True, True, True),
	),
	(
		# chapter 3
		("122985", True, True, True),
	),
	(
		# chapter 4
		("122986", True, True, True),
	),
	(
		# chatper 5
		("122989", True, True, True),
	),
	(
		# chapter 6
		("122990", True, True, True),
	),
	(
		# chapter 7
		("122991", True, True, True),
	),
	(
		# chapter 8
		("122992", True, True, True),
	),
	(
		# chapter 9
		("122993", True, True, True,),
		("122994", False, False, False,),
		("122995", False, False, False,),
	),
	(
		# chapter 10
		("122996", True, True, True,),
		("122997", False, False, False),
		("122998", False, False, False),
		("123000", False, False, False),
	),
	(
		# chapter 11
		("123001", True, True, True,),
		("123002", False, False, False,),
		("123003", False, False, False),
		("123004", False, False, False),
		("123005", False, False, False),
	),
	(
		# chapter 12
		("123006", True, True, True),
	),
	(
		# chapter 13
		("123010", True, True, True),
		("123011", False, False, False),
		("123012", False, False, False),
		("123013", False, False, False),
		("123014", False, False, False),
		("123015", False, False, False),
		("123016", False, False, False),
		("123017", False, False, False),
		("123019", False, False, False),
		("123020", False, False, False),
	),
]

def get_url(id):
	return BASEURL + "&uid=" + id

def fetch():
	import urllib, os
	basedir = os.path.dirname(__file__) or '.'
	for i, chapter in enumerate(SOURCES):

		dirname = os.path.sep.join((basedir, "%02d"%(i+1)))
		if not os.path.isdir(dirname):
			os.makedirs(dirname)
		for j, item in enumerate(chapter):
			id = item[0]
			url = get_url(id)
			filename = os.path.sep.join((dirname, '%02d'%(j+1)))
			if os.path.isfile(filename):
				print 'skip ', url
				continue
			print 'fetching from', url
			u = urllib.urlopen(url)
			s = u.read()
			print >>open(filename, "w"), s

if __name__ == '__main__':
	fetch()
