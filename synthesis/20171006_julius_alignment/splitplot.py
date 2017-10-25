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
    # accfile = "/home/akiyama/synthesis/20171006_julius_alignment/accphrase/" + fn[0:3] + "/" + fn + ".txt"
    # labfile = "/home/akiyama/synthesis/20171006_julius_alignment/out/" + fn + ".lab"
    # splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/" + fn + ".lab"

    accfile = "/Users/akiyamatakanori/Desktop/dialect_synthesis/synthesis/20171006_julius_alignment/accphrase/" + fn[0:3] + "/" + fn + ".txt"
    labfile = "/Users/akiyamatakanori/Desktop/dialect_synthesis/synthesis/20171006_julius_alignment/out/" + fn + ".lab"
    splitfile = "/Users/akiyamatakanori/Desktop/dialect_synthesis/synthesis/20171006_julius_alignment/split/" + fn + ".lab"

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
    acctimestart += [phonemestart[-1]]
    acctimeend += [phonemeend[-1]]
    accphrase += ["sil"]

    fw = open(splitfile, "w")

    print(accphrase)

    for j in range(len(accphrase)):
        fw.write(str(acctimestart[j]))
        fw.write(" ")
        fw.write(str(acctimeend[j]))
        fw.write(" ")
        fw.write(accphrase[j])

    timelength = phonemeend[-1]

    fw.close()

    continuousF0file = "/Users/akiyamatakanori/Desktop/dialect_synthesis/synthesis/20171006_julius_alignment/continuousF0/NF" + fn + "_DT.txt"
    continuousF0 = np.loadtxt(continuousF0file)

    framelength = len(continuousF0)

    sr = timelength / framelength

    print(len(accphrase))

    #fft_cf0 = np.zeros(0)

    # font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
    # font_prop = FontProperties(fname=font_path)
    # matplotlib.rcParams['font.family'] = font_prop.get_name()

    for k in range(len(accphrase)):
        sub_cf0 = continuousF0[int(acctimestart[k]/sr):int(acctimeend[k]/sr)]
        sub_fft_cf0 = np.fft.fft(sub_cf0)
        # plt.subplot(4,4,k+1)
        # plt.plot(np.abs(sub_fft_cf0))

    cf0 = continuousF0[int(acctimestart[7]/sr):int(acctimeend[7]/sr)]
    print(cf0)
    fft_cf0 = np.fft.fft(cf0)
    cut_fft_cf0 = fft_cf0[0:50]
    cut_cf0 = np.fft.ifft(cut_fft_cf0)
    print(abs(cut_cf0))

    plt.subplot(2,1,1)
    plt.plot(cf0)
    plt.subplot(2,1,2)
    plt.plot(cut_cf0)
    plt.show()

    #print(framelength)



    # plt.show()

    # plt.ylim(4,6)
    # plt.plot(continuousF0, label='continuous log F0')
    # plt.legend()
    #
    # for k in range(len(accphrase)):
    #     plt.plot([acctimestart[k]*framelength/timelength,acctimestart[k]*framelength/timelength],[4,6],'k-', linewidth=0.5)
    #     plt.text((acctimestart[k]+acctimeend[k])*framelength/(2*timelength), 4.2, str(accphrase[k]), fontsize=12, ha='center', va ='center')
    #
    # plt.plot([acctimeend[len(accphrase) - 1]*framelength/timelength,acctimeend[len(accphrase) - 1]*framelength/timelength],[4,6],'k-', linewidth=0.5)
    # plt.show()
    #plt.savefig("001007.jpg")


