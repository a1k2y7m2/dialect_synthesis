#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties

# accfile = "/home/akiyama/synthesis/20171006_julius_alignment/accphrase/001/001007.txt"
# labfile = "/home/akiyama/synthesis/20171006_julius_alignment/out/001007.lab"
# splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/001007.lab"

for r in open("test.scp").readlines():
    fn = r.strip()
    accfile = "/home/akiyama/synthesis/20171006_julius_alignment/accphrase/" + fn[0:3] + "/" + fn + ".txt"
    labfile = "/home/akiyama/synthesis/20171006_julius_alignment/out/" + fn + ".lab"
    splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/" + fn + ".lab"

    accstart = []
    accend = []
    accphrase = []

    acctimestart = []
    acctimeend = []

    #load phoneme-time relation

    phonemestart = []
    phonemeend = []
    for l in open(labfile).readlines():
        data = l.split(' ')
        phonemestart += [float(data[0])]
        phonemeend += [float(data[1])]

    # add silS to list
    acctimestart += [phonemestart[0]]
    acctimeend += [phonemeend[0]]
    accphrase += ["sil\n"]


    #load accent phrase-word relation

    for a in open(accfile).readlines():
        data = a.split(' ')
        accstart += [int(data[0])]
        accend += [int(data[1])]
        accphrase += [data[2]]


    #time-accphrase relation

    for i in range(len(accphrase) - 1):
        acctimestart += [phonemestart[accstart[i]]]
        acctimeend += [phonemeend[accend[i]]]


    # add silE to list
    acctimestart += [phonemestart[len(phonemestart) - 1]]
    acctimeend += [phonemeend[len(phonemeend) - 1]]
    accphrase += ["sil"]

    fw = open(splitfile, "w")

    print(accphrase)

    for j in range(len(accphrase)):
        fw.write(str(acctimestart[j]))
        fw.write(" ")
        fw.write(str(acctimeend[j]))
        fw.write(" ")
        fw.write(accphrase[j])

    timelength = phonemeend[len(phonemeend) - 1]

    fw.close()

    continuousF0file = "/home/akiyama/synthesis/20171006_julius_alignment/continuousF0/NF" + fn + "_DT.txt"
    continuousF0 = np.loadtxt(continuousF0file)

    #ploting

    framelength = len(continuousF0)
    #print(framelength)

    font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
    font_prop = FontProperties(fname=font_path)
    matplotlib.rcParams['font.family'] = font_prop.get_name()

    plt.ylim(4,6)
    plt.plot(continuousF0, label='continuous log F0')
    plt.legend()

    for k in range(len(accphrase)):
        plt.plot([acctimestart[k]*framelength/timelength,acctimestart[k]*framelength/timelength],[4,6],'k-', linewidth=0.5)
        plt.text((acctimestart[k]+acctimeend[k])*framelength/(2*timelength), 4.2, str(accphrase[k]), fontsize=12, ha='center', va ='center')

    plt.plot([acctimeend[len(accphrase) - 1]*framelength/timelength,acctimeend[len(accphrase) - 1]*framelength/timelength],[4,6],'k-', linewidth=0.5)
    plt.show()
    #plt.savefig("001007.jpg")


