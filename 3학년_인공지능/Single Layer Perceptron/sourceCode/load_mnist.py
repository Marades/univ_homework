# -*- coding: utf-8 -*-

import os
import os.path as op
import struct as st
import numpy as np
import random as ra
import matplotlib.pyplot as plt



# MNIST 데이터 경로
#_SRC_PATH = u'mnist\\raw_binary'
_TRAIN_DATA_FILE = '../train-images.idx3-ubyte'
_TRAIN_LABEL_FILE = '../train-labels.idx1-ubyte'
_TEST_DATA_FILE = '../t10k-images.idx3-ubyte'
_TEST_LABEL_FILE = '../t10k-labels.idx1-ubyte'

# MNIST 데이터 크기 (28x28)
_N_ROW = 28                 # 세로 28픽셀
_N_COL = 28                 # 가로 28픽셀
_N_PIXEL = _N_ROW * _N_COL

# 출력 이미지 경로
_DST_PATH = './img_gray'



def drawImage(dataArr, fn):
    fig, ax = plt.subplots()
    ax.imshow(dataArr, cmap='gray')
    #plt.show()
    plt.savefig(fn)
    
    
    
def loadData(fn):
    print 'loadData', fn
    
    fd = open(fn, 'rb')
    
    # header: 32bit integer (big-endian)
    magicNumber = st.unpack('>I', fd.read(4))[0]
    nData = st.unpack('>I', fd.read(4))[0]
    nRow = st.unpack('>I', fd.read(4))[0]
    nCol = st.unpack('>I', fd.read(4))[0]
    
    print 'magicNumber', magicNumber
    print 'nData', nData
    print 'nRow', nRow
    print 'nCol', nCol
    
    # data: unsigned byte
    dataList = []
    for i in range(nData):
        dataRawList = fd.read(_N_PIXEL)
        dataNumList = st.unpack('B' * _N_PIXEL, dataRawList)
        dataArr = np.array(dataNumList).reshape(_N_ROW, _N_COL)
        dataList.append(dataArr.astype('float32') / 255.0)
        
    fd.close()
    
    print 'done.'
    print
    
    return dataList
    


def loadLabel(fn):
    print 'loadLabel', fn
    
    fd = open(fn, 'rb')
    
    # header: 32bit integer (big-endian)
    magicNumber = st.unpack('>I', fd.read(4))[0]
    nData = st.unpack('>I', fd.read(4))[0]
    
    print 'magicNumber', magicNumber
    print 'nData', nData
    
    # data: unsigned byte
    labelList = []
    for i in range(nData):
        dataLabel = st.unpack('B', fd.read(1))[0]
        labelList.append(dataLabel)
        
    fd.close()
    
    print 'done.'
    print
    
    return labelList



def loadMNIST():
    # 학습 데이터 / 레이블 로드
    trDataList = loadData(_TRAIN_DATA_FILE)
    trLabelList = loadLabel(_TRAIN_LABEL_FILE)
    
    # 테스트 데이터 / 레이블 로드
    tsDataList = loadData(_TEST_DATA_FILE)
    tsLabelList = loadLabel(_TEST_LABEL_FILE)
    
    return trDataList, trLabelList, tsDataList, tsLabelList

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output
 
def sigmoid_output_to_derivative(output):
    return output*(1-output)    
    
if __name__ == '__main__':
    trDataList, trLabelList, tsDataList, tsLabelList = loadMNIST()
    
    print 'len(trDataList)', len(trDataList)
    print 'len(trLabelList)', len(trLabelList)
    print 'len(tsDataList)', len(tsDataList)
    print 'len(tsLabelList)', len(tsLabelList)
    
    if op.exists(_DST_PATH) == False:
        os.mkdir(_DST_PATH)
    
    weight = np.random.rand(784, 10)
    rho = 0.7
    epoch = 100
    times = 100
    cnt = 0
    # 샘플로 5개씩만 출력해보기
    for t in range(times):
        tempdataArr = []
        labelArr = []
        for i in range(epoch):
            label = trLabelList[cnt + i]
            labelArr.append(label)
            #dstFn = _DST_PATH + u'\\tr_%d_label_%d.png' % (i, label)
            #print '%d-th train data: label=%d' % (i, label)
            #drawImage(trDataList[i], dstFn)
            #dstFn = _DST_PATH + u'\\tr_%d_label_%d.txt' % (i, label)
            
            #np.savetxt(dstFn, trDataList[i], fmt='%4d')
            
            byteArr = np.array(trDataList[cnt + i])
            tempArr = []
            for j in range(0, 28):
                for k in range(0, 28):
                    tempArr.append(byteArr[j][k])
            tempdataArr.append(tempArr)
            
        cnt += epoch
        dataArr = np.array(tempdataArr).reshape(784, epoch)

        dot = np.dot(weight.T, dataArr)
        o = sigmoid(dot/100)
 
        
        sum = 0
        for k in range(epoch):
            answer = np.argmax(o.T[k])
            if answer == labelArr[k]:
                sum += 1
                print '%d-epoch s %d-sample label: %d   result: %d -> correct' % (t, k, labelArr[k], answer)
            else:
                print '%d-epoch s %d-sample label: %d   result: %d -> wrong' % (t, k, labelArr[k], answer)
        print sum
        # for j in range(784):
            # for k in range(10):
                # for l in range(epoch):
                    # la = np.zeros(10)
                    # la[labelArr[l]] = 1
                    # weight[j][k] = weight[j][k] + rho*(labelArr[k] - o[k][l])*o[k][l]*(1-o[k][l])*dataArr[j][l]

    for i in range(5):
        label = tsLabelList[i]
        dstFn = _DST_PATH + u'\\ts_%d_label_%d.png' % (i, label)
        #print '%d-th test data: label=%d' % (i, label)
        drawImage(tsDataList[i], dstFn)
        
        dstFn = _DST_PATH + u'\\ts_%d_label_%d.txt' % (i, label)
        np.savetxt(dstFn, tsDataList[i], fmt='%4d')
        