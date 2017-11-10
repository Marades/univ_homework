import os
import os.path as op
import struct as st
import numpy as np
import random as ra
import pickle as pkl
# MNIST 데이터 경로
#_SRC_PATH = u'mnist\\raw_binary'
_TEST_DATA_FILE = '../t10k-images.idx3-ubyte'
_TEST_LABEL_FILE = '../t10k-labels.idx1-ubyte'

# MNIST 데이터 크기 (28x28)
_N_ROW = 28                 # 세로 28픽셀
_N_COL = 28                 # 가로 28픽셀
_N_PIXEL = _N_ROW * _N_COL

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
    # 테스트 데이터 / 레이블 로드
    tsDataList = loadData(_TEST_DATA_FILE)
    tsLabelList = loadLabel(_TEST_LABEL_FILE)
    
    return tsDataList, tsLabelList

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output

if __name__ == '__main__':
    #MNIST에서 테스트 데이터 불러옴
    tsDataList, tsLabelList = loadMNIST()
    print 'len(tsDataList)', len(tsDataList)
    print 'len(tsLabelList)', len(tsLabelList)
    #베스트 파라미터 로드
    weight = load('best_param.pkl')
    #test_output파일 쓰기 형식으로 오픈
    fd = open('test_output.txt', 'w')
    #testData 맞은 갯수
    lastResult = 0
    for i in range(10000):
        #현재 데이터 라벨 저장
        label = tsLabelList[i]
        #현재 데이터 샘플 저장
        tbyteArr = np.array(tsDataList[i])
        #tempArr에 바이어스와 불러온 데이터를 합하여 저장 후 dataArr에 numpy의 array로 저장
        tempArr = []
        tempArr.append(1)
        for j in range(0, 28):
            for k in range(0, 28):
                tempArr.append(tbyteArr[j][k])       
        dataArr = np.array(tempArr)
        
        #불러온 weight와 데이터로 계산
        dot = np.dot(weight.T, dataArr.T)
        o = sigmoid(dot/100)
        #인식된 정답값 저장
        answer = np.argmax(o.T)
        #정답 여부 확인 및 파일에 기록
        fd.write(str(i) + "'s sample : " + str(label) + ' -> ' + str(answer))
        if answer == label:
            lastResult += 1
            fd.write('success\n')
            print '%d-sample label: %d   result: %d -> correct' % (i, label, answer)
        else:
            print '%d-sample label: %d   result: %d -> wrong' % (i, label, answer)
            fd.write('failure\n') 
    #정답 개수 출력 및 최종 결과 파일에 기록   
    print lastResult        
    fd.write('Rate : ' + str(lastResult) + ' / 10000 (' + str(float(lastResult/10000)) + '%)')