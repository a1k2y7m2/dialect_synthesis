#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import numpy as np
import chainer
import chainer.functions as F
import chainer.links as L
import argparse
import math
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from chainer import cuda, training

vocab_size = 8000
n_units = 64
out_size = 50
EPOCH_NUM = 2000

#network definition
class LSTM(chainer.Chain):
    def __init__(self, in_size, n_units, out_size, train=True):
        super(LSTM, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(in_size, n_units)
            self.l1 = L.LSTM(n_units, n_units)
            self.l2 = L.LSTM(n_units, n_units)
            self.l3 = L.Linear(n_units, out_size)

        for param in self.params():
            param.data[...] = np.random.uniform(-0.1, 0.1, param.data.shape)

    def reset_state(self):
        self.l1.reset_state()
        self.l2.reset_state()

    def __call__(self,x):
        h0 = self.embed(x)
        h1 = self.l1(F.dropout(h0))
        h2 = self.l2(F.dropout(h1))
        y = self.l3(F.dropout(h2))
        return y

    def lossfun(self, x, t):
        y = self.__call__(x)
        return F.mean_squared_error(y, t)

def load_input(inputfile):
    subword_id = np.loadtxt(inputfile,delimiter=" ",dtype=np.int32)
    return subword_id

def load_output(outputfile):
    output = np.loadtxt(outputfile,delimiter=",",dtype=np.float32)
    mean = output.mean()
    output -= mean*np.ones(output.shape)
    return output


class BiGRU(chainer.Chain):
    def __init__(self, in_size, n_units, out_size, train=True):
        super(BiGRU, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(in_size, n_units)
            self.hf = L.GRU(n_units, n_units)
            self.hb = L.GRU(n_units, n_units)
            self.l3 = L.Linear(n_units*2, out_size)

        for param in self.params():
            param.data[...] = np.random.uniform(-0.1, 0.1, param.data.shape)

    def reset_state(self):
        self.hf.reset_state()
        self.hb.reset_state()

    def __call__(self,x_list):
        h0_list = list(map(self.embed,x_list))
        f1_list = []
        b1_list = []
        for h0 in h0_list:
            f1_list.append(self.hf(F.dropout(h0)))
        for rh0 in reversed(h0_list):
            b1_list.append(self.hb(F.dropout(rh0[::-1])))
        b1_list = b1_list[::-1]
        h1_list = [chainer.Variable(np.c_[f1_list[i].data,b1_list[i].data]) for i in range(len(f1_list))]
        y_list = []
        for h1 in h1_list:
            y = self.l3(F.dropout(h1))
            y_list.append(y)

        return y_list

    def lossfun(self, x_list, t_list):
        y_list = self.__call__(x_list)
        loss = 0
        for i in range(len(y_list)):
            loss += F.mean_squared_error(y_list[i], t_list[i])
        return loss


parser = argparse.ArgumentParser()
parser.add_argument('--gpu', '-g', default=-1, type=int, help='GPU ID (negative value indicates CPU)')
parser.add_argument('--model', '-m', default="LSTM", type=str, help='Model Name(LSTM or BiGRU)')
args = parser.parse_args()

def main():

    if args.gpu >= 0:
        # Make a specified GPU current
        chainer.cuda.get_device_from_id(args.gpu).use()
        chainer.cuda.check_cuda_available()
        #xp = cuda.cupy
    else:
        xp = np

    if args.model == "LSTM":
        model = LSTM(vocab_size,n_units,out_size)
    elif args.model == "BiGRU":
        model = BiGRU(vocab_size,n_units,out_size)
    if args.gpu >= 0:
        model.to_gpu()

    # Setup an optimizer
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)
    st = datetime.datetime.now()
    for epoch in range(EPOCH_NUM):

        for r in open("train.scp").readlines():
            fn = r.strip()
            inputfile = "./train_in/" + fn + ".sub"
            outputfile = "./train_out/" + fn + ".csv"
            subwordseq = load_input(inputfile)
            f0seq = load_output(outputfile)
            model.reset_state()
            model.cleargrads()
            loss = 0
            if args.model == "LSTM":
                for i in range(len(f0seq)):
                    x = chainer.Variable(np.array([subwordseq[i]]))
                    t = chainer.Variable(np.array([f0seq[i]]))
                    loss += model.lossfun(x,t)
            if args.model == "BiGRU":
                x_list = []
                t_list = []
                for i in range(len(f0seq)):
                    x_list.append(chainer.Variable(np.array([subwordseq[i]])))
                    t_list.append(chainer.Variable(np.array([f0seq[i]])))
                loss += model.lossfun(x_list,t_list)

        loss.backward()
        optimizer.update()
        if (epoch+1)%100 == 0:
            ed = datetime.datetime.now()
            print("epoch:\t{}\tloss:\t{}\ttime:\t{}\t".format(epoch+1,loss.data,ed-st))
            st = datetime.datetime.now()

    #plot raw f0 and predicted f0

    predict = np.empty(0)
    # for i in range(len(f0seq)):
    #     y = model(chainer.Variable(np.array([subwordseq[i]], dtype=np.int32)))
    #     predict = np.r_[predict, y.data[0][:]]

    y_list = model(x_list)
    for i in range(len(f0seq)):
        predict = np.r_[predict, y_list[i].data[0][:]]


    #####################plot########################

    # font_path = '/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf'
    # font_prop = FontProperties(fname=font_path)
    # matplotlib.rcParams['font.family'] = font_prop.get_name()
    #
    # splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/" + fn + ".lab"
    # subword = []
    # for k in range(len(f0seq)):
    #     l = open(splitfile).readlines()[k+1].strip().split(" ")
    #     subword += [l[2]]
    #
    # for k in range(len(f0seq)):
    #     plt.plot([out_size*(k + 1),out_size*(k + 1)],[-1,1],'k-', linewidth=0.5)
    #     plt.text(out_size*(k + 0.5), -1, str(subword[k]), fontsize=12, ha='center', va ='center')

    plt.plot(predict,label="predicted F0")
    plt.plot(f0seq.reshape((1,-1))[0][:],label="raw F0")

    plt.show()


if __name__ == '__main__':
    main()