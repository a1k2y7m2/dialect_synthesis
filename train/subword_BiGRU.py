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

n_layer = 2
vocab_size = 8000
n_units = 64
out_size = 50
EPOCH_NUM = 2000
batch_size = 1

def load_input(inputfile):
    subword_id = np.loadtxt(inputfile,delimiter=" ",dtype=np.int32)
    return subword_id

def load_output(outputfile):
    output = np.loadtxt(outputfile,delimiter=",",dtype=np.float32)
    # mean = output.mean()
    # output -= mean*np.ones(output.shape)
    return output

class BiGRU(chainer.Chain):
    def __init__(self, n_layer, in_size, n_units, out_size, dropout=0.5):
        super(BiGRU, self).__init__()
        with self.init_scope():
            self.embed = L.EmbedID(in_size, n_units)
            self.l1 = L.NStepBiGRU(n_layer, n_units, n_units, dropout)
            self.l2 = L.Linear(n_units*2, out_size)

    def __call__(self, x_list):
        h0_list = list(map(self.embed, x_list))
        hx = None
        hy, h1_list = self.l1(hx, h0_list)
        y_list = []
        for h1 in h1_list:
            y = self.l2(F.dropout(h1))
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
args = parser.parse_args()

def main():

    if args.gpu >= 0:
        # Make a specified GPU current
        chainer.cuda.get_device_from_id(args.gpu).use()
        chainer.cuda.check_cuda_available()
        xp = cuda.cupy
    else:
        xp = np

    model = BiGRU(n_layer,vocab_size,n_units,out_size)
    if args.gpu >= 0:
        model.to_gpu()
        #model.using_config('use_cudnn', use_cudnn)

    # Setup an optimizer
    optimizer = chainer.optimizers.Adam()
    optimizer.setup(model)

    print("#vocab =", vocab_size)

    #loading train_data
    # data is the list of the list of "chainer.Variable"
    input = []
    output = []

    for r in open("train.scp").readlines():
        fn = r.strip()
        inputfile = "./train_in/" + fn + ".sub"
        outputfile = "./train_out/" + fn + ".csv"
        subwordseq = load_input(inputfile)
        f0seq = load_output(outputfile)
        model.cleargrads()
        loss = 0

        train_x_list = []
        train_t_list = []
        for i in range(len(f0seq)):
            train_x_list.append(xp.array([subwordseq[i]]))
            train_t_list.append(xp.array([f0seq[i]]))

        input.append(train_x_list)
        output.append(train_t_list)

    input = xp.asarray(input)
    output = xp.asarray(output)

    n_text = len(input)
    print("#n_text =", n_text)
    st = datetime.datetime.now()
    for epoch in range(EPOCH_NUM):

        perm = np.random.permutation(n_text)
        all_loss = 0
        for i in range(0, n_text, batch_size):
            loss = 0
            input_list = input[perm[i:i+batch_size]]
            output_list = output[perm[i:i+batch_size]]
            model.cleargrads()
            for j in range(batch_size):
                x_list = [xp.asarray(item, dtype=xp.int32) for item in input_list[j]]
                t_list = [xp.asarray(item, dtype=xp.float32) for item in output_list[j]]
                loss += model.lossfun(x_list, t_list)

            all_loss += loss
            loss.backward()
            optimizer.update()
        if (epoch + 1) % 100 == 0:
            ed = datetime.datetime.now()
            print("epoch:\t{}\tloss:\t{}\ttime:\t{}\t".format(epoch+1,all_loss.data,ed-st))
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