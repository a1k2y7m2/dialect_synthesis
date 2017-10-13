#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import codecs

# sys.stdin = codecs.getreader('utf-8')(sys.stdin)
# sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

parser = argparse.ArgumentParser()
parser.add_argument('targetfile', type=str, help='target file(e.g.001_KAN.txt)')

args = parser.parse_args()

sentencenum = 0
for text in open("/home/akiyama/JNAS/JNAS1/OriginalText/KANJI/NP_unlabeled/" + args.targetfile).readlines():
    sentencenum += 1
    text = text.rstrip()
    splittext = " ".join(text.decode('utf-8'))

    fw = open("/home/akiyama/JNAS/JNAS_txtsplit/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum) + ".align", "w")
    fw.write(splittext.encode('utf-8'))
    fw.close()


fp = open("/home/akiyama/JNAS/align_data/" + args.targetfile.rstrip("_KAN.txt") + ".jp-ph", "w")

for i in range(sentencenum):
    jptxt = open("/home/akiyama/JNAS/JNAS_txtsplit/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(i + 1) + ".align", "r").read()
    phtxt = open("/home/akiyama/JNAS/JNAS_phoneme_align/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(i + 1) + ".align", "r").read()

    fp.write(jptxt)
    fp.write(" ||| ")
    fp.write(phtxt)
    fp.write('\n')
fp.close()