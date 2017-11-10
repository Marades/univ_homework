import matplotlib.pyplot as plt
import random
import numpy as np
import sys
import os.path as op

def runExp(popSize, eliteNum, mutProb):
    print 'training...'
    trResFn = 'train_Log_%d_%d_%.2f' % (popSize, eliteNum, mutProb)
    print 'result file:', trResFn
    print 'testing...'
    tsResFn = 'test_output_%d_%d_%.2f' % (popSize, eliteNum, mutProb)
    print 'result file:', tsResFn

if __name__ == '__main__':
    
    #command line argument로 전체 개체 수, 다음 세대에 유지될 Elite개체 수, Mutation확률을 입력받음
    argmentNum = len(sys.argv)
    
    if argmentNum == 4:
        popSize = int(sys.argv[1])
        eliteNum = int(sys.argv[2])
        mutProb = float(sys.argv[3])
        
        runExp(popSize, eliteNum, mutProb)
    else:
        print ('Usage: %s [populationSize] [eliteNum]' '[mutationProb]') % (op.basename(sys.argv[0]))
    
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
    
    #각각 a, b, c의 유전자를 가진 전체개체를 나타내는 2차원 배열 생성 - 초기유전자값은 일정범위내에서 랜덤으로 부여
    chromosomeList = [[0 for col in range(3)] for row in range(popSize)]
    for i in range(0, popSize):
        chromosomeList[i][0] = random.uniform(-100, 100)
        chromosomeList[i][1] = random.uniform(-100, 100)
        chromosomeList[i][2] = random.uniform(-200, 0)
    
    #학습로그를 저장할 파일을 쓰기형식으로 open함
    fd = open('train_log_[' + str(popSize) + ']_[' + str(eliteNum) + ']_[' + str(mutProb) + '].txt', 'w') 
    fd.write('세대별 Elite들의 유전자 및 오류율\n')
    #세대를 나타내는 변수
    generation = 0
    #학습을 위한 while문
    while True:
        #각 개체의 에러율을 저장할 배열
        errRate = []
        #학습을 위해 주어진 파라미터로 오류율 계산후 각각의 오류율 저장
        for i in range(0, popSize):
            a = chromosomeList[i][0]
            b = chromosomeList[i][1]
            c = chromosomeList[i][2]
            err = 0
            for fish in salmon:
                if(a*fish[0] + b*fish[1] + c > 0):
                    err += 1
            
            for fish in seabass:
                if(a*fish[0] + b*fish[1] + c < 0):
                    err += 1  
            errRate.append(err)
        
        #오류율을 저장한 배열을 오름차순으로 배열
        minIndex = np.argsort(errRate) #print minIndex        
        fd.write('generation : ' + str(generation) + ' \n')
        #전 세대에서 가장 에러열이 낮은 개체를 eliteNum만큼 유지
        for i in range(0, eliteNum):
            chromosomeList[i][0] = chromosomeList[minIndex[i]][0]
            chromosomeList[i][1] = chromosomeList[minIndex[i]][1]
            chromosomeList[i][2] = chromosomeList[minIndex[i]][2]
            fd.write('  ' + str(i) + ' 번째 elite의 유전자')
            fd.write('  a : ' + str(chromosomeList[i][0]) + '\n  b : ' + str(chromosomeList[i][1]) + '\n  c : '  + str(chromosomeList[i][2]) + '\n')
            fd.write('  ' + str(i) + ' 번째 elite의 errRate : ' + str(errRate[minIndex[i]]) + '\n')
       
        #세대 증가
        generation += 1

        #에러가 일정 수준 이하로 내려가면 break로 학습 중단
        if(err <= 10):
             break
        
        #남은 개체들을 Mutation확률을 고려해서 윗세대에서 유전시킴
        for i in range(eliteNum, popSize):
            mutant = random.uniform(0, 100)
            #랜덤으로 만든 값이 입력받은 mutProb보다 클 경우 정상대로 유전
            if (mutant >= mutProb):
                #부모 선택
                pnt = []
                ran = random.randint(0,99)
                if(ran > 40):
                    pnt.append(random.randint(0,eliteNum - 1))
                else:
                    pnt.append(random.randint(eliteNum - 1, popSize - 1))
                ran = random.randint(0,99)
                if(ran > 40):
                    pnt.append(random.randint(0,eliteNum - 1))
                else:
                    pnt.append(random.randint(eliteNum - 1, popSize - 1))
                #위에서 선택된 부모에게 랜덤으로 유전자 물려받음
                ran = random.randint(0,1)
                chromosomeList[i][0] = chromosomeList[pnt[ran]][0]
                ran = random.randint(0,1)
                chromosomeList[i][1] = chromosomeList[pnt[ran]][1]
                ran = random.randint(0,1)
                chromosomeList[i][2] = chromosomeList[pnt[ran]][2]
            #랜덤으로 만든 값이 입력받은 mutProb보다 작은 경우 mutation발생
            else:
                chromosomeList[i][0] = random.uniform(-100, 100)
                chromosomeList[i][1] = random.uniform(-100, 100)
                chromosomeList[i][2] = random.uniform(-200, 0)

    fd.write('=======Train Result========\n')
    fd.write('전체 개체 수 : ' + str(popSize) + '\tElite개체 수 : ' + str(eliteNum) + '\tMutation확률 : ' + str(mutProb) + '\n')
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
    fd = open('test_output_[' + str(popSize) + ']_[' + str(eliteNum) + ']_[' + str(mutProb) + '].txt', 'w')
    
    #salmon과 seabass가 올바르게 분류되었을 경우 잘못 분류되었을 경우를 저장할 각각의 배열을 만든다.
    salmonGood = []
    salmonBad = []
    seabassGood = []
    seabassBad = []
    
    #오류율을 저장할 변수를 선언한다.
    err = 0.0
    
    best_a = chromosomeList[0][0]
    best_b = chromosomeList[0][1]
    best_c = chromosomeList[0][2]
    
    #위에서 얻은 최적의 Parameter로 salmon과 seabass의 분류하여 파일에 기록한다.
    for sal in testSalmon:
        if (best_a * (sal[0]) + best_b * (sal[1]) + best_c) <= 0:
            salmonGood.append([sal[0], sal[1]])
            fd.write('body : ' + str(sal[0]) + '     tail : ' + str(sal[1]) + '(salmon) ==> salmon        (correct)\n')
        else:
            salmonBad.append([sal[0], sal[1]])
            fd.write('body : ' + str(sal[0]) + '     tail : ' + str(sal[1]) + '(salmon) ==> seabass        (error)\n')
            err+=1
            
    for bass in testSeabass:
        if (best_a * (bass[0]) + best_b * (bass[1]) + best_c) >= 0:
            seabassGood.append([bass[0], bass[1]])
            fd.write('body : ' + str(bass[0]) + '     tail : ' + str(bass[1]) + '(seabass) ==> seabass        (correct)\n')
        else:
            seabassBad.append([bass[0], bass[1]])
            fd.write('body : ' + str(bass[0]) + '     tail : ' + str(bass[1]) + '(seabass) ==> salmon        (error)\n')
            err+=1
    
    #분류 결과를 콘솔에 대략적으로 출력하고 파일에 자세히 기록한 후 파일을 닫는다.
    print 'generation : ', generation, 'errRate : ', err
    fd.write('=======Test Result========\n')
    fd.write('전체 개체 수 : ' + str(popSize) + '\tElite개체 수 : ' + str(eliteNum) + '\tMutation확률 : ' + str(mutProb) + '\n')
    fd.write('errorRate = ' + str(err) + '% (' + str(err) + '/100)\n')
    fd.close()