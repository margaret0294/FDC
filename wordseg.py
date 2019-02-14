#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, codecs
import jieba.posseg as pseg
#word segmentation

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 wordseg.py infile outfile")
        sys.exit()
    i = 0
    infile, outfile = sys.argv[1:3]
    output = codecs.open(outfile, 'w', 'utf-8')
    with codecs.open(infile, 'r', 'utf-8') as myfile:
        for line in myfile:
            i = i + 1
            line = line.strip()
            words = pseg.cut(line)
            for word, flag in words:
                output.write(word + ' ')
            output.write('\n')
            if (i % 1000 == 0):
                print('Finished ' + str(i) + ' lines')
    output.close()
    print('Finished ')
