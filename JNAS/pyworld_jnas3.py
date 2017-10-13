#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test script of pyworld
"""

import pyworld as pw
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import argparse

HTS_U_SYMBOL = -1e+10

parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str, help='target directory(e.g. F001')
parser.add_argument('inputwav', type=str, help='the name of dataset file')

args = parser.parse_args()

def rm_micro_prosody(lf0, n_frame=4):
   if len(np.where(lf0 == HTS_U_SYMBOL)[0]) != 0:
      raise ValueError("unvoiced frames are included.")

   smooth_lf0 = np.zeros(len(lf0))
   for t in range(len(lf0)):
      smooth_lf0[t] = np.average(lf0[max(t - n_frame, 0): min(t + n_frame + 1, len(lf0) - 1)])

   return smooth_lf0

def lf02clf0(lf0, smooth=False):
   clf0 = np.zeros(len(lf0))
   t = np.arange(len(lf0))
   t_voiced = t[np.where(lf0 != HTS_U_SYMBOL)]
   lf0_voiced = lf0[t_voiced]

   # uv
   uv = np.zeros(len(lf0))
   uv[t_voiced] = 1

   # smoothing & interpolation
   contlf0 = interp1d(t_voiced, lf0_voiced)  # lienar interpolation
   clf0[t_voiced[0]:t_voiced[-1] + 1] = contlf0(np.arange(t_voiced[0], t_voiced[-1] + 1))
   clf0[t_voiced[0]:t_voiced[-1] + 1] = rm_micro_prosody(clf0[t_voiced[0]:t_voiced[-1] + 1])

   # smoothing & extrapolation
   clf0[:t_voiced[0]] = lf0[t_voiced[0]]
   clf0[t_voiced[-1] + 1:] = lf0[t_voiced[-1]]
   clf0 = rm_micro_prosody(clf0)

   # restore voiced frames
   clf0[t_voiced] = lf0[t_voiced]

   # smoothing (trajectory smoothing)
   if smooth is True:
      clf0 = rm_micro_prosody(clf0)

   return clf0, uv

def clf02lf0(clf0, uv):
   lf0 = np.ones(len(clf0)) * HTS_U_SYMBOL
   lf0[np.where(uv == 1)] = clf0[np.where(uv == 1)]

   return lf0

def f02lf0(f0, inv=False):
   x = []
   if inv:
      for f in lf0:
         x.append(np.exp(f) if f == HTS_U_SYMBOL else 0.)
   else:
      for f in f0:
         x.append(np.log(f) if f > 0. else HTS_U_SYMBOL)
   return np.array(x)

if __name__ == "__main__":
    wavfile = "/home/akiyama/JNAS/JNAS3/WAVES_DT/" + args.directory + "/NP/" + args.inputwav
    fs, data = read(wavfile)
    #print("Sampling rate : ",fs)
    print(args.inputwav)
    floatdata = data.astype(np.float64)

    f0, sp, ap = pw.wav2world(floatdata, fs)

    #----plot-----

    # fig = plt.figure()
    #
    # ax1 = fig.add_subplot(3,1,1)
    # ax2 = fig.add_subplot(3,1,2)
    # ax3 = fig.add_subplot(3,1,3)
    #
    # ax1.plot(floatdata)
    # ax2.plot(f0)

    lf0 = f02lf0(f0)  # log F0
    clf0, uv = lf02clf0(lf0, smooth=True)  # continuous log F0

    # ax3.plot(lf0, label="original log F0")
    # ax3.plot(clf0, label="continuous log F0")
    # plt.ylim(4, 6)
    # plt.legend()
    # plt.show()

    np.savetxt("/home/akiyama/JNAS/JNAS_voicedata/WAVES_DT/" + args.directory + "/" + args.inputwav.replace(".wav", ".txt"), clf0, delimiter=",")



