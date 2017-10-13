#!/usr/bin/env python
"""
script of subword embedding model
"""

import chainer.links as L
import numpy as np

data = np.genfromtxt("JNAS_ID_subword.csv", delimiter=",")
data[np.isnan(data)] = 0 #convert Nan to 0
data = data.astype('i')
print(data)

embedding_size = 30
l = L.EmbedID(8000,embedding_size)
y = l(data)
print(y.data)