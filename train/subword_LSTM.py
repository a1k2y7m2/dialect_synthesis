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
import matplotlib.pyplot as plt

vocab_size = 8000
n_units = 30
out_size = 171
EPOCH_NUM = 2000

#network definition
class LSTM(chainer.Chain):
    def __init__(self, in_size, n_units, out_size, train=True):
        super(LSTM, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(in_size, n_units)
            self.l1 = L.LSTM(n_units, n_units)
            self.l2 = L.Linear(n_units, out_size)

    def reset_state(self):
        self.l1.reset_state()

    def __call__(self,x):
        h0 = self.embed(x)
        h1 = self.l1(h0)
        y = self.l2(h1)
        return y

    def lossfun(self, x, t):
        y = self.__call__(x)
        return F.mean_squared_error(y, t)

def load_input(inputfile):
    subword_id = np.loadtxt(inputfile,delimiter=" ",dtype=np.int32)
    return subword_id

def load_output(outputfile):
    output = np.loadtxt(outputfile,delimiter=",",dtype=np.float32)
    return output





parser = argparse.ArgumentParser()
parser.add_argument('--gpu', '-g', default=-1, type=int, help='GPU ID (negative value indicates CPU)')
args = parser.parse_args()

def main():

    if args.gpu >= 0:
        # Make a specified GPU current
        chainer.cuda.get_device_from_id(args.gpu).use()
        chainer.cuda.check_cuda_available()

    model = LSTM(vocab_size,n_units,out_size)

    if args.gpu >= 0:
        model.to_gpu()

    # Setup an optimizer
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)

    for epoch in range(EPOCH_NUM):
        st = datetime.datetime.now()
        for r in open("train.scp").readlines():
            fn = r.strip()
            inputfile = "/home/akiyama/synthesis/train/train_in/" + fn + ".sub"
            outputfile = "/home/akiyama/synthesis/train/train_out/" + fn + ".csv"
            subwordseq = load_input(inputfile)
            f0seq = load_output(outputfile)
            model.reset_state()
            model.cleargrads()
            loss = 0
            for i in range(len(f0seq)):
                x = chainer.Variable(np.array([subwordseq[i]]))
                t = chainer.Variable(np.array([f0seq[i]]))
                loss += model.lossfun(x,t)
            loss.backward()
            optimizer.update()
            ed = datetime.datetime.now()
            print("epoch:\t{}\tloss:\t{}\ttime:\t{}\t".format(epoch+1,loss.data,ed-st))
            st = datetime.datetime.now()

    y = model.__call__(chainer.Variable(np.array([1],dtype = np.int32)))
    plt.plot(y.data[0][:])
    plt.plot(f0seq[1])
    plt.show()


if __name__ == '__main__':
    main()