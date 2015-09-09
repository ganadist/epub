from __future__ import print_function

BASEURL="http://data.navercast.naver.com/literature_module/30/"

def get_url(id):
	return BASEURL + 'literature_44_%d.html'%id

def fetch():
	import urllib, os
	basedir = os.path.dirname(__file__) or '.'
	dirname = os.path.sep.join((basedir, "source"))
	if not os.path.isdir(dirname):
		os.makedirs(dirname)
	for i in range(1, 49):
		filename = os.path.sep.join((dirname, "%02d"%i))
		url = get_url(i)
		if os.path.isfile(filename):
			print('skip', url)
			continue
		print('fetching from', url)
		u = urllib.urlopen(url)
		s = u.read()
		print(s, file=open(filename, "w"))

if __name__ == '__main__':
	fetch()
