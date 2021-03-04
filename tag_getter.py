import os
import json

header = '''# Tags in folder

This file is auto-generated, remove the tags in the code, not
here. It searches through the files in a directory and finds all 'tags' in the
format ##TAG: (tag text). A tag can be ended with ## or :
(##TAG: (tag text): (Not part of the tag)):
'''

def _valid_tag(tag):
    for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 0, '.'):
        n = str(n)
        tag = tag.replace(n, '')
    return tag.isupper()

def get_tags(from_):
    try: file = open(from_)
    except: file = from_.splitlines()
    tags = {}
    for line in file:
        if '##' in line:
            Check = line.split('##')[-1]
            try: a, b = Check.split(':')[:2]
            except: continue
            if _valid_tag(a):
                if tags.get(a):
                    tags[a].append(b.strip())
                    continue
                tags[a] = [b.strip()]
    return tags

def getall():
    list = os.listdir()
    pylist = [n for n in list if n.endswith('.py')]
    pytags = dict([(py, get_tags(py)) for py in pylist])
    return pytags

def add_tags_to(file, /, can_overwrite = False):
    if can_overwrite: file = open(file, 'w')
    else: file = open(file, 'x')
    file.write(header)
    tags = getall()
    for py, ntags in tags.items():
        file.write('\n')
        file.write('## '+py+'\n')
        for tagname, tag_content in ntags.items():
            file.write('\n### '+tagname+'\n\n')
            for tag in tag_content:
                file.write('    '+tag+'\n')
    file.close()
