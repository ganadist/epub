# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re

ID_PAT = u'^#(?P<id>\d+)\.'
ID_REF = re.compile(ID_PAT)
LINK_PAT = u'#(?P<id>\d+)(로|으로) 가시오'
LINK_REF = re.compile(LINK_PAT)

def get_paragraph(filename):
    b = BeautifulSoup(open(filename))
    for item in b.select('table tr td'):
        if 'word-break:break-all; padding:8;' == item.get('style'):
            break
    else:
        return []

    # body
    contents = item.contents

    def x(item):
        return isinstance(item, NavigableString)
    # filter string
    contents = filter(x, contents)
    # filter '&nbsp;'
    return map(lambda x:x.replace('&nbsp;', ' '), contents)

def hook_chapter_6(line):
    matched = ID_REF.match(line.strip())
    if matched:
        return {'tag': 'p',
            'id': 'part' + matched.group('id'),
            'text': line}
    matched = re.match(LINK_REF, line.strip())
    if u'로 가시오' in line:
        print(line)
    return line
  

def get_chapter(filename, isFirst = False):
    if isFirst:
        has_title, has_chapter, has_quote = True, True, True
    else:
        has_title, has_chapter, has_quote = False, False, False

    found_chapter = False
    found_quote = False
    quote = []

    chapter = ''
    p = []
    paragraph = get_paragraph(filename)

    if '06/' in filename:
        hook = hook_chapter_6
    else:
        hook = lambda x: x

    if has_title:
        # find and drop title
        if isinstance(paragraph, list): # python2
            paragraph = paragraph[1:]
        else: # python3
            next(paragraph)

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
                if line[2:].startswith(u'\xa0' * 10):
                    p.append({
                        'tag': 'blockquote',
                        'children': quote,
                    })
                    p.append({
                        'text':line.strip(),
                        'class':'text-right'
                    })
                    p.append(None) # page break
                    found_quote = True
                    continue
                quote.append(line.strip())
            continue

        if line.strip().startswith('--------'):
            break

        p.append(hook(line))

    return chapter, p

if __name__ == '__main__':
    import sys
    for i, filename in enumerate(sys.argv[1:]):
        #print '\nCR\n'.join(get_paragraph(filename))
        get_chapter(filename, i == 0)

