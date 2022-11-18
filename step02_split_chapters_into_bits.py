import os
import re


def openfile(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def savefile(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def yield_chunks(lines, count):
    result = list()
    chunk = list()
    for l in lines:
        l = l.strip()
        chunk.append(l)
        if len(chunk) >= count and len(l) == 0:
            text = '\n'.join(chunk)
            result.append(text)
            chunk = list()
    return result


if __name__ == '__main__':
    files = os.listdir('chapters/')
    for file in files:
        chapter = openfile('chapters/%s' % file)
        lines = chapter.splitlines()
        chunks = yield_chunks(lines, 90)
        idx = 0
        for chunk in chunks:
            if len(chunk) > 5000:
                continue
            if len(chunk) < 3500:
                continue
            if idx<10:
                filename = file.replace('.txt', '_00%s.txt' % str(idx))
            elif idx<100:
                filename = file.replace('.txt', '_0%s.txt' % str(idx))
            else:
                filename = file.replace('.txt', '_%s.txt' % str(idx))
            idx += 1
            savefile('chapter_bits/%s' % filename, chunk.strip())