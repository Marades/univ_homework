import matplotlib.pyplot as plt
import random
import numpy as np
import sys
import os.path as op

def runExp(learningRate):
    print 'training...'
    trResFn = 'train_Log_%.2f' % (learningRate)
    print 'result file:', trResFn
    print 'testing...'
    tsResFn = 'test_output_%.2f' % (learningRate)
    print 'result file:', tsResFn

if __name__ == '__main__':
    
    #command line argument로 learningRate를 입력받음
    argmentNum = len(sys.argv)
    
    if argmentNum == 2:
        learningRate = float(sys.argv[1])
        runExp(learningRate)
    else:
        print ('Usage: %s [learningRate]') % (op.basename(sys.argv[0]))
    
    #학습용 salmon_train.txt파일을 읽기 형식으로 열어 값을 저장한 후 파일을 닫음
    fd = open('salmon_train.txt', 'r')
    lines = fd.readlines()
    fd.close()
    
    #salmonList배열에 몸길이와 꼬리길이를 나누어 저장함
    salmonList = []
    for line in lines:
        temp1 = line.split()
        salmonList.append([temp1[0], temp1[1], 0])
    
    #학습용 seabass_train.txt파일을 읽기 형식으로 열어 값을 저장한 후 파일을 닫음
    fd = open('seabass_train.txt', 'r')
    lines = fd.readlines()
    fd.close()        
 
    #seabassList배열에 몸길이와 꼬리길이를 나누어 저장함 
    seabassList = []
    for line in lines:
        temp2 = line.split()
        seabassList.append([temp2[0], temp2[1], 1])
    
    #salmon과 seabass배열에 map함수를 이용하여 각 배열값을 float형으로 바꿔 저장함
    salmon = []
    seabass = []
    for s in salmonList:
        salmon.append(map(float, s))
    for s in seabassList:
        seabass.append(map(float, s))
    
    #weight배열을 선언하여 임의의 값 저장
    weight = [random.uniform(-50, 50), random.uniform(-50, 50), random.uniform(-200, 0)]
    #Cost Function의 값을 저장할 변수 선언
    ok = 0
    #학습로그를 저장할 파일을 쓰기형식으로 open함
    fd = open('train_log_[' + str(learningRate) + '].txt', 'w') 
    fd.write('세대별 Elite들의 유전자 및 오류율\n')
    #세대를 나타내는 변수
    generation = 0
    #입력받은 학습률 저장
    rho = learningRate
    #학습을 위한 while문
    while True:
        #각 개체의 에러율을 저장할 배열
        #학습을 위해 주어진 파라미터로 오류율 계산후 각각의 오류율 저장
        err = 0
        for fish in salmon:
            if(weight[0]*fish[0] + weight[1]*fish[1] + weight[2] > 0):
                err += 1
                ok = 1
                weight[0] = weight[0] + rho*(0 - ok)*fish[0]
                weight[1] = weight[1] + rho*(0 - ok)*fish[1]
                weight[2] = weight[2] + rho*(0 - ok)*fish[2]
            generation += 1
            fd.write('weight : ' + str(weight[0]) + ', ' + str(weight[1]) +  ', ' + str(weight[2]) + '\n')
        
        for fish in seabass:
            if(weight[0]*fish[0] + weight[1]*fish[1] + weight[2] < 0):
                err += 1  
                ok = 0
                weight[0] = weight[0] + rho*(1 - ok)*fish[0]
                weight[1] = weight[1] + rho*(1 - ok)*fish[1]
                weight[2] = weight[2] + rho*(1 - ok)*fish[2]
            generation += 1
            fd.write('weight : ' + str(weight[0]) + ', ' + str(weight[1]) +  ', ' + str(weight[2]) + '\n')

        #에러가 일정 수준 이하로 내려가면 break로 학습 중단
        if(err <= 10):
             break
        

    fd.write('=======Train Result========\n')
    fd.write('Learning Rate : ' + str(learningRate) + '\n')
    fd.write('generation : ' + str(generation) + '\n')
    fd.write('weight : ' + str(weight[0]) + ', ' + str(weight[1]) +  ', ' + str(weight[2]) + '\n')
    fd.write('errorRate = ' + str(err) + '% (' + str(err) + '/100)\n')
    fd.close()
    ############################
    
    
    #salmon_test.txt파일과 seabass_test.txt파일을 열어 몸길이와 꼬리길이를 나누어 각각
    #tmpSalmon과 tmpSeabass배열에 저장하고 파일을 닫는다.
    fd = open('salmon_test.txt', 'r')
    lines = fd.readlines()
    fd.close()
    
    tmpSalmon = []
    for line in lines:
        tmpSalmon.append(line.split())
        
    fd = open('seabass_test.txt', 'r')
    lines = fd.readlines()
    fd.close()
    
    tmpSeabass = []
    for line in lines:
        tmpSeabass.append(line.split())    
    
    #testSalmon배열과 testSeabass배열에 tmpSalmon과 tmpSeabass배열에 들어가 있는 값을 float형으로 바꿔 저장한다.
    testSalmon = []
    testSeabass = []
    for s in tmpSalmon:
        testSalmon.append(map(float, s))
    for s in tmpSeabass:
        testSeabass.append(map(float, s))
    
    #파일을 쓰기형식으로 연다.
    fd = open('test_output_[' + str(learningRate) + '].txt', 'w')
    
    #salmon과 seabass가 올바르게 분류되었을 경우 잘못 분류되었을 경우를 저장할 각각의 배열을 만든다.
    salmonGood = []
    salmonBad = []
    seabassGood = []
    seabassBad = []
    
    #오류율을 저장할 변수를 선언한다.
    err = 0.0
    
    
    #위에서 얻은 최적의 Parameter로 salmon과 seabass의 분류하여 파일에 기록한다.
    for sal in testSalmon:
        if (weight[0] * (sal[0]) + weight[1] * (sal[1]) + weight[2]) <= 0:
            salmonGood.append([sal[0], sal[1]])
            fd.write('body : ' + str(sal[0]) + '     tail : ' + str(sal[1]) + '(salmon) ==> salmon        (correct)\n')
        else:
            salmonBad.append([sal[0], sal[1]])
            fd.write('body : ' + str(sal[0]) + '     tail : ' + str(sal[1]) + '(salmon) ==> seabass        (error)\n')
            err+=1
            
    for bass in testSeabass:
        if (weight[0] * (bass[0]) + weight[1] * (bass[1]) + weight[2]) >= 0:
            seabassGood.append([bass[0], bass[1]])
            fd.write('body : ' + str(bass[0]) + '     tail : ' + str(bass[1]) + '(seabass) ==> seabass        (correct)\n')
        else:
            seabassBad.append([bass[0], bass[1]])
            fd.write('body : ' + str(bass[0]) + '     tail : ' + str(bass[1]) + '(seabass) ==> salmon        (error)\n')
            err+=1
    
    #분류 결과를 콘솔에 대략적으로 출력하고 파일에 자세히 기록한 후 파일을 닫는다.
    print 'generation : ', generation, 'errRate : ', err
    fd.write('=======Test Result========\n')
    fd.write('Learning Rate : ' + str(learningRate) + '\n')
    fd.write('errorRate = ' + str(err) + '% (' + str(err) + '/100)\n')
    fd.close()
    
    ##########3
    fig, ax = plt.subplots()
    
    #올바르게 분류된 salmon을 녹색 삼각형으로 표시하도록 한다.
    xlist = []
    ylist = []
    for data in salmonGood:
        x, y = data
        xlist.append(x)
        ylist.append(y)
    ax.plot(xlist, ylist, 'g^', label = 'salmon_corr')
    
    #잘못 분류된 salmon을 적색 삼각형으로 표시하도록 한다.
    xlist = []
    ylist = []
    for data in salmonBad:
        x, y = data
        xlist.append(x)
        ylist.append(y)
    ax.plot(xlist, ylist, 'r^', label = 'salmon_wrong')
    
     #올바르게 분류된 seabass을 녹색 사각형으로 표시하도록 한다.
    xlist = []
    ylist = []
    for data in seabassGood:
        x, y = data
        xlist.append(x)
        ylist.append(y)
    ax.plot(xlist, ylist, 'gs', label = 'seabass_corr')
    
    #잘못 분류된 salmon을 적색 사각형으로 표시하도록 한다.
    xlist = []
    ylist = []
    for data in seabassBad:
        x, y = data
        xlist.append(x)
        ylist.append(y)
    ax.plot(xlist, ylist, 'rs', label = 'seabass_wrong')
    
    ax.grid(True)
    ax.legend(loc='upper right')
    ax.set_xlabel('length of body')
    ax.set_ylabel('length of tail')
    ax.set_xlim((None, None))
    ax.set_ylim((None, None))
    
    #결과를 test_output.png파일로 저장하고 보여준다.
    plt.savefig('test_output.png')
    plt.show()