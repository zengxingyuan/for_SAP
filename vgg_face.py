import caffe
import numpy as np
from PIL import Image
import scipy.misc

MODEL_FILE = './VGG_FACE_deploy.prototxt'
PRETRAIN_FILE = './VGG_FACE.caffemodel'

net = caffe.Net(MODEL_FILE, PRETRAIN_FILE, caffe.TEST)
    
def isSame(a, b):
    return scipy.spatial.distance.cosine(a, b) <= 0.3

def faceToVector(filename):
    img = scipy.misc.imresize(caffe.io.load_image(filename), (224, 224))
    img = img[:,:,::-1] # convert RGB->BGR
    avg = np.array([129.1863,104.7624,93.5940])
    img = img - avg # subtract mean
    img = img.transpose((2,0,1)) 
    img = img[None,:] # add singleton dimension
    net.forward_all( data = img )
    return np.copy(net.blobs['fc8'].data[0])
