import matplotlib.pyplot as plt
import random
import numpy

if __name__ == '__main__':
    
    #학습용 salmon_train.txt파일을 읽기 형식으로 열어 값을 저장한 후 파일을 닫음
    fd = open('salmon_train.txt', 'r')
    lines = fd.readlines()
    fd.close()
    
    #salmonList배열에 몸길이와 꼬리길이를 나누어 저장함
    salmonList = []
    for line in lines:
        temp1 = line.split()
        salmonList.append([temp1[0], temp1[1]])
    
    #학습용 seabass_train.txt파일을 읽기 형식으로 열어 값을 저장한 후 파일을 닫음
    fd = open('seabass_train.txt', 'r')
    lines = fd.readlines()
    fd.close()        
 
    #seabassList배열에 몸길이와 꼬리길이를 나누어 저장함 
    seabassList = []
    for line in lines:
        temp2 = line.split()
        seabassList.append([temp2[0], temp2[1]])
    
    #salmon과 seabass배열에 map함수를 이용하여 각 배열값을 float형으로 바꿔 저장함
    salmon = []
    seabass = []
    
    for s in salmonList:
        salmon.append(map(float, s))
    for s in seabassList:
        seabass.append(map(float, s))
    
    
    #각 시도마다 변하는 Parameter값을 저장할 배열 선언
    a = []
    b = []
    c = []
    
    #초기 온도값
    T = 100
    #각 시도마다의 에러율을 저장하는 배열
    ErrRate = []
    #Parameter의 첫값에 2, -1, -180을 저장함
    a.append(2.0)
    b.append(-1.0)
    c.append(-180.0)
    #시도횟수를 나타내는 변수 선언
    count = 0

    #학습 과정을 저장할 train_log.txt 파일을 쓰기 형식으로 연다
    fd = open('train_log.txt', 'w')
    
    #온도가 0.001보다 작아질 때까지 학습을 반복한다.
    while True:
        #에러 횟수 저장하는 변수 errCnt 선언
        errCnt = 0
        
        #각각의 salmon과 seabass가 선형분류기로 나눠지는 영역에 올바르게 속해있지 않을 경우 errCnt를 1 증가시킨다.
        for item in salmon:
            if (a[count]*item[0] + b[count]*item[1] + c[count]) > 0:
                errCnt += 1
        for item in seabass:
            if (a[count]*item[0] + b[count]*item[1] + c[count]) < 0:
                errCnt += 1
        
        #에러 횟수를 배열에 저장한다.
        ErrRate.append(errCnt)

        #현재의 Parameter에서 랜덤한 값을 더하여 새로 Parameter배열에 추가시킨다.
        a.append(a[count] + random.uniform(-0.01, +0.01))
        b.append(b[count] + random.uniform(-0.01, +0.01))
        c.append(c[count] + random.uniform(-10.0, +10.0))
        
        #몇번째 시도에 에러율이 어떻게 되는지 콘솔에 출력하고 train_log.txt파일에 기록한다.
        fd.write(str(count) + '-th traing, T = ' + str(T) + ', ErrorRate = ' + str(errCnt) + '% (' + str(errCnt) + '/100)\n')
        print count, '-th traing ErrRate : ', errCnt, '%'
        
        #횟수를 1 증가시키고 온도를 0.99배로 낮춘다.
        count += 1
        T *= 0.99
        
        #온도가 0.001보다 낮아질 경우 반복문 탈출
        if T < 0.001:
            break

    #에러율이 가장 낮았을 때의 Parameter를 저장한다.
    best_a = a[ErrRate.index(min(ErrRate))]
    best_b = b[ErrRate.index(min(ErrRate))]
    best_c = c[ErrRate.index(min(ErrRate))]
    
    #가장 에러율이 낮을 때의 에러율과 Parameter값을 train_log.txt 파일에 기록하고 파일을 닫는다.
    fd.write('best parameter = [' + str(best_a) + ', ' + str(best_b) + ', ' + str(best_c) + ']\n')
    fd.write('best errorRate = ' + str(min(ErrRate)) + '%\n')
    fd.close()
    
    #salmon_test.txt파일과 seabass_test.txt파일을 열어 몸길이와 꼬리길이를 나누어 각각
    #tmpSalmon과 tmpSeabass배열에 저장하고 파일을 닫는다..
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
    
    #test_output.txt파일을 쓰기형식으로 연다.
    fd = open('test_output.txt', 'w')
    
    #salmon과 seabass가 올바르게 분류되었을 경우 잘못 분류되었을 경우를 저장할 각각의 배열을 만든다.
    salmonGood = []
    salmonBad = []
    seabassGood = []
    seabassBad = []
    
    #오류율을 저장할 변수를 선언한다.
    err = 0.0
    
    #위에서 얻은 최적의 Parameter로 salmon과 seabass의 분류하여 그 결과를 콘솔에 출력하고 test_output.txt파일에 기록한다.
    for sal in testSalmon:
        if (best_a * (sal[0]) + best_b * (sal[1]) + best_c) <= 0:
            salmonGood.append([sal[0], sal[1]])
            print 'body : ', sal[0], '     tail : ', sal[1], '(salmon) ==> salmon        (correct)'
            fd.write('body : ' + str(sal[0]) + '     tail : ' + str(sal[1]) + '(salmon) ==> salmon        (correct)\n')
        else:
            salmonBad.append([sal[0], sal[1]])
            print 'body : ', sal[0], '     tail : ', sal[1], '(salmon) ==> seabass        (error)'
            fd.write('body : ' + str(sal[0]) + '     tail : ' + str(sal[1]) + '(salmon) ==> seabass        (error)\n')
            err+=1
            
    for bass in testSeabass:
        if (best_a * (bass[0]) + best_b * (bass[1]) + best_c) >= 0:
            seabassGood.append([bass[0], bass[1]])
            print 'body : ', bass[0], '     tail : ', bass[1], '(seabass) ==> seabass        (correct)'
            fd.write('body : ' + str(bass[0]) + '     tail : ' + str(bass[1]) + '(seabass) ==> seabass        (correct)\n')
        else:
            seabassBad.append([bass[0], bass[1]])
            print 'body : ', bass[0], '     tail : ', bass[1], '(seabass) ==> salmon        (error)'
            fd.write('body : ' + str(bass[0]) + '     tail : ' + str(bass[1]) + '(seabass) ==> salmon        (error)\n')
            err+=1
    
    #test케이스의 오류율을 콘솔에 출력하고 test_output.txt파일에 기록한 후 파일을 닫는다.
    print 'errorRate = ', err, '% (', err, '/100)'
    fd.write('=======Test Result========\n')
    fd.write('errorRate = ' + str(err) + '% (' + str(err) + '/100)\n')
    fd.close()
    
    ######################################
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
    