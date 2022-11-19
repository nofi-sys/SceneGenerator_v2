import os
import re


def openfile(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def savefile(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


if __name__ == '__main__':
    files = os.listdir('books/')
    for file in files:
        book = openfile('books/%s' % file)
        #book = book.split('START OF THE PROJECT GUTENBERG')[1]
        #book = book.split('END OF THE PROJECT GUTENBERG')[0]
        chapters = book.split('CHAPTER')
        result = list()
        for chapter in chapters:
            chunks = re.split('(\*\s{4,})+\*', chapter)
            result += chunks
        result2 = list()
        for r in result:
            chunks = re.split('\s{4,}[XVIVI]+\s{4,}', r)
            result2 += chunks
        idx = 0
        for chapter in result2:
            #### SKIP IF TOO SHORT
            chapter = chapter.strip()
            if len(chapter) < 2000:
                continue
            #### COMPILE FILENAME & SAVE
            if idx<10:
                filename = file.replace('.txt', '_00%s.txt' % str(idx))
            elif idx<100:
                filename = file.replace('.txt', '_0%s.txt' % str(idx))
            else:
                filename = file.replace('.txt', '_%s.txt' % str(idx))
            idx += 1
            savefile('chapters/%s' % filename, chapter.strip())