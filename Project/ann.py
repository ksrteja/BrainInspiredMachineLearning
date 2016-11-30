import matplotlib.pyplot as plt
from sklearn.datasets import fetch_mldata
from sklearn.neural_network import MLPClassifier
import os, struct
from array import array as pyarray
import numpy as np
from numpy import array, int8, uint8, zeros

def load_mnist_60000(dataset="training", digits=np.arange(10), path="."):
    if dataset == "training":
        fname_img = 'C:/Users/Prash/Desktop/psych268_bilm-master/code/train-images.idx3-ubyte'
        fname_lbl = 'C:/Users/Prash/Desktop/psych268_bilm-master/code/train-labels.idx1-ubyte'
    elif dataset == "testing":
        fname_img = os.path.join(path, 't10k-images.idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    flbl = open(fname_lbl, 'rb')
    magic_nr, size = struct.unpack(">II", flbl.read(8))
    lbl = pyarray("b", flbl.read())
    flbl.close()

    fimg = open(fname_img, 'rb')
    magic_nr, size, rows, cols = struct.unpack(">IIII", fimg.read(16))
    img = pyarray("B", fimg.read())
    fimg.close()

    ind = [ k for k in range(size) if lbl[k] in digits ]
    N = len(ind)

    images = zeros((N, rows, cols), dtype=uint8)
    labels = zeros((N, 1), dtype=int8)
    for i in range(len(ind)):
        images[i] = array(img[ ind[i]*rows*cols : (ind[i]+1)*rows*cols ]).reshape((rows, cols))
        labels[i] = lbl[ind[i]]

    return images, labels
    
data, labels = load_mnist_60000('training', digits=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], path=os.path.dirname(os.path.abspath(__file__)))  #200 sample
data = (data.T / (data.T).sum(axis=0)).T

data = data.reshape(60000, 784)
data = data/np.float32(256)

NUM_TRAIN = 200
NUM_TEST = 10
X_train, X_test = data[:NUM_TRAIN], data[NUM_TRAIN:NUM_TRAIN + NUM_TEST]
y_train, y_test = labels[:NUM_TRAIN], labels[NUM_TRAIN:NUM_TRAIN + NUM_TEST]

mlp = MLPClassifier(hidden_layer_sizes=(100000), max_iter=100000, alpha=1e-9,
                    solver='sgd', verbose=10, random_state=1,
                    learning_rate_init=.1)

mlp.fit(X_train, y_train)
print("Training set score: %f" % mlp.score(X_train, y_train))
print("Test set score: %f" % mlp.score(X_test, y_test))