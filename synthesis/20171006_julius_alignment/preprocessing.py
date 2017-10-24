#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
from maxlength import maxlength
import scipy as sp
#from pylab import show
from scipy import interpolate
import math

#deciding F0 fixed length according to the number of mora
alpha = 2
#deciding modulated spectrum liftering according to the number of mora
beta = 0.5

inplen = math.ceil(maxlength().max_mora_length("train.scp")*alpha)

def normalize(continuousF0,axis=None):
    cmean = continuousF0.mean(axis=axis, keepdims=True)
    cstd = np.std(continuousF0, axis=axis, keepdims=True)
    zscore = (continuousF0-cmean)/cstd
    return zscore

def resampling(sub_lpf_cf0,inplen):
    t = np.linspace(0,1,len(sub_lpf_cf0))
    tt = np.linspace(0,1,inplen)
    f_inter = interpolate.interp1d(t, sub_lpf_cf0, kind='cubic')
    us_sub_lpf_cf0 = f_inter(tt)
    # plt.plot(t,sub_lpf_cf0,'--')
    # plt.plot(tt,us_sub_lpf_cf0,'-')
    # plt.show()

    return us_sub_lpf_cf0

def define_LPF_threshold(katphrase, modspe):
    moranum = maxlength().mora_length(katphrase)
    threshold = math.floor(moranum*beta + 1)

    return threshold

fp = open("traindata.scp","w")

for r in open("train.scp").readlines():
    fn = r.strip()
    accfile = "/home/akiyama/synthesis/20171006_julius_alignment/accphrase/" + fn[0:3] + "/" + fn + ".txt"
    labfile = "/home/akiyama/synthesis/20171006_julius_alignment/out/" + fn + ".lab"
    splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/" + fn + ".lab"
    traindatafile = "/home/akiyama/synthesis/20171006_julius_alignment/traindata/" + fn + ".csv"

    accstart = []
    accend = []
    accphrase = []
    katphrase = []

    acctimestart = []
    acctimeend = []

    #load phoneme-time relation

    phonemestart = []
    phonemeend = []
    for l in open(labfile).readlines():
        data = l.split(' ')
        phonemestart += [float(data[0])]
        phonemeend += [float(data[1])]
    if len(phonemestart) == 0:
        print(fn,".lab is None.")
        continue

    # add silS to list
    acctimestart += [phonemestart[0]]
    acctimeend += [phonemeend[0]]
    accphrase += ["sil\n"]
    katphrase += ["sil"]


    #load accent phrase-word relation

    for a in open(accfile).readlines():
        data = a.strip().split(' ')
        accstart += [int(data[0])]
        accend += [int(data[1])]
        accphrase += [data[2]+"\n"]
        if len(data) < 4:
            katphrase += [['pau']]
        else:
            katphrase += [data[3]]

    #time-accphrase relation

    for i in range(len(accphrase) - 1):
        acctimestart += [phonemestart[accstart[i]]]
        acctimeend += [phonemeend[accend[i]]]


    # add silE to list
    acctimestart += [phonemestart[-1]]
    acctimeend += [phonemeend[-1]]
    accphrase += ["sil"]
    katphrase += ["sil"]

    fw = open(splitfile, "w")

    for j in range(len(accphrase)):
        fw.write(str(acctimestart[j]))
        fw.write(" ")
        fw.write(str(acctimeend[j]))
        fw.write(" ")
        fw.write(accphrase[j])

    timelength = phonemeend[-1]

    fw.close()

    continuousF0file = "/home/akiyama/synthesis/20171006_julius_alignment/continuousF0/NF" + fn + "_DT.txt"
    continuousF0 = np.loadtxt(continuousF0file)

    framelength = len(continuousF0)
    nomF0 = normalize(continuousF0)

    sr = timelength / framelength

    #fft_cf0 = np.zeros(0)

    font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'

    font_prop = FontProperties(fname=font_path)
    matplotlib.rcParams['font.family'] = font_prop.get_name()
    input = np.zeros((len(accphrase)-2, inplen))
    for k in range(1, len(accphrase)-1):
        sub_cf0 = nomF0[int(acctimestart[k]/sr):int(acctimeend[k]/sr)]
        #If subword's mora equals zero, make inplen'th array which has the same number.
        if len(sub_cf0) == 0:
            sub_cf0 = nomF0[int(acctimestart[k]/sr)]**np.ones((1,inplen)).flatten()

        rs_sub_cf0 = resampling(sub_cf0, inplen)
        modspe = np.fft.fft(rs_sub_cf0)
        threshold = define_LPF_threshold(katphrase[k], modspe)
        for j in range(threshold,len(modspe)):
            modspe[j] = 0
        sub_lpf_cf0 = np.real(np.fft.ifft(modspe))

        #input initial length
        #a = np.array([len(sub_lpf_cf0)])
        input[k-1][:] = sub_lpf_cf0

        # if k == 3:
        #     plt.plot(rs_sub_cf0)
        #     print(sub_lpf_cf0)
        #     plt.plot(sub_lpf_cf0)
        #     plt.show()

    np.savetxt(traindatafile,input,delimiter=",")
    print(fn,".csv is rightly generated!")
    fp.write(fn)
    fp.write("\n")

fp.close()

    # plt.show()

    # plt.ylim(4,6)
    # plt.plot(continuousF0, label='continuous log F0')
    # #plt.plot(lpf_cf0, label='LPF continuous log F0')
    # plt.legend()
    # #
    # for k in range(len(accphrase)):
    #     plt.plot([acctimestart[k]*framelength/timelength,acctimestart[k]*framelength/timelength],[4,6],'k-', linewidth=0.5)
    #     plt.text((acctimestart[k]+acctimeend[k])*framelength/(2*timelength), 4.2, str(katphrase[k]), fontsize=12, ha='center', va ='center')
    #
    # plt.plot([acctimeend[len(accphrase) - 1]*framelength/timelength,acctimeend[len(accphrase) - 1]*framelength/timelength],[4,6],'k-', linewidth=0.5)
    # plt.show()
    #plt.savefig("001007.jpg")