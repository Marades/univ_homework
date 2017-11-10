# -*- coding: utf-8 -*-
import os
import os.path as op
import struct as st
import numpy as np
import random as ra
import pickle as pkl
# MNIST 데이터 경로
#_SRC_PATH = u'mnist\\raw_binary'
_TRAIN_DATA_FILE = '../train-images.idx3-ubyte'
_TRAIN_LABEL_FILE = '../train-labels.idx1-ubyte'

# MNIST 데이터 크기 (28x28)
_N_ROW = 28                 # 세로 28픽셀
_N_COL = 28                 # 가로 28픽셀
_N_PIXEL = _N_ROW * _N_COL

# 출력 이미지 경로
_DST_PATH = './img_gray'

def save(fn, obj):
    fd = open(fn, 'wb')
    pkl.dump(obj, fd)
    fd.close()
    
def load(fn):
    fd = open(fn, 'rb')
    obj = pkl.load(fd)
    fd.close()
    return obj
    
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
        dataList.append(dataArr.astype('float32') / 255.0)  #255로 나누어 0~1사이의 실수값으로 바꿈
        
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
    
    return trDataList, trLabelList

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output
 
if __name__ == '__main__':
    trDataList, trLabelList = loadMNIST()
    
    print 'len(trDataList)', len(trDataList)
    print 'len(trLabelList)', len(trLabelList)

    
    #바이어스와 28X28개의 데이터에 해당하는 weight배열 생성
    weight = np.random.rand(785, 10)
    rho = 0.7   #학습율
    times = 60000 #60000개 데이터 받아오기
    epoch = 3 #60000 단위 몇 번 반복할지
    
    fd = open('train_log.txt', 'w')
    for t in range(epoch):
        tempdataArr = []#일시적으로 데이터 담을 배열
        sum = 0         #트레이닝 단계에서 맞은 수
        
        fd.write('-----------------------------')
        fd.write('epoch : ' + str(t) + '\n')
        for i in range(times):
            correct = 0                         #현재 샘플을 맞췄는지 아닌지
            label = trLabelList[i]              #현재 데이터 라벨 저장
            byteArr = np.array(trDataList[i])   #트레이닝 데이타 정보를 Numpy의 array로 저장
            
            tempArr = []
            tempArr.append(1)       #bias추가
            #tempArr에 정보 저장
            for j in range(0, 28):
                for k in range(0, 28):
                    tempArr.append(byteArr[j][k])
            #numpy의 array 형식으로 dataArr에 tempArr저장
            dataArr = np.array(tempArr)
            
            #weight와 배열 내적하여 계산
            dot = np.dot(weight.T, dataArr.T)
            o = sigmoid(dot/100)
            #계산된 값에서 가장 큰 인덱스 저장 -> 인식된 숫자
            answer = np.argmax(o.T)
            #인식된 숫자가 정답일 경우 맞은 갯수 sum 1 증가
            if answer == label:
                sum += 1
                correct = 1
            
            #라벨을 나타내는 One-Hot Representation
            la = np.zeros(10)
            la[label] = 1
            for j in range(785):
                for k in range(10):
                    weight[j][k] = weight[j][k] + rho*(la[k] - o[k])*o[k]*(1-o[k])*dataArr[j]
                    
            fd.write(str(i) + "'s sample : " + str(label) + ' -> ' + str(answer))
            if correct == 1:
                fd.write('success\n')
            else:
                fd.write('failure\n')
        print sum
        fd.write('Rate : ' + str(sum) + ' / 60000\n')

        #학습률 decay
        rho *= 0.99
    fd.close()
    save('best_param.pkl', weight)