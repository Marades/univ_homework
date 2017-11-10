# -*- coding: utf-8 -*-

import numpy as np

def sigmoid(x):
    output = 1/(1+np.exp(-x))
    return output
    
trainData = np.array([[1, 1, 1, 1], [0, 0, 1, 1], [0, 1, 0, 1]])    #트레이닝 데이터
testData = np.array([[1, 1, 1, 1], [0, 0, 1, 1], [0, 1, 0, 1]])     #테스트 테이터
answerLabel = [0, 1, 1, 0]                                          #XOR 정답 라벨
if __name__ == '__main__':

    #시드 설정
    np.random.seed(0)
    #초기 Weight 생성
    tempWeight1 = np.random.rand(3, 2)
    tempWeight2 = np.random.rand(3)
    #생성한 weight를 numpy의 array로 변환
    weight1 = np.array(tempWeight1)
    weight2 = np.array(tempWeight2)
    #첫 번째와 두 번째 weight학습률
    rho1 = 0.8
    rho2 = 0.8

    epoch = 0                         #세대 수
    fd = open('train_log.txt', 'w')   #training 과정 기록할 파일    
    answerCount = 0                   #연속으로 정답을 맞추는 횟수를 저장
    while(True):        
        
        ans = 0     #한 epoch sample내에서 정답 맟춘 개수
        
        #h1에 계산한 값을 저장 하고 h1에 bias를 추가하여 히든레이어를 나타내는 h 생성
        h1 = sigmoid(np.dot(weight1.T, trainData))
        h = np.zeros((3, 4))
        h[0] = [1, 1, 1, 1]
        h[1] = h1[0]
        h[2] = h1[1]
        
        #o에 ouput layer의 값 저장
        o = sigmoid(np.dot(weight2.T, h))
        
        #각각의 sample의 최종 output값과 label값을 비교하여 차이가 일정 수준 이하로 갈 때까지 학습, 차이가 일정 수준 밑이면 정답
        for i in range(4):
            if abs(answerLabel[i] - o[i]) < 0.2:
                ans += 1

        #결과 파일 및 콘솔에  출력
        fd.write('epoch : ' + str(epoch) +'\n')
        print 'epoch : ', epoch
        fd.write('1st weight : ')
        for i in range(3):
            for j in range(2):
                fd.write(str(weight1[i][j]) + ' ')
        fd.write('\n2nd weight : ')
        for i in range(3):
            fd.write(str(weight2[i]) + ' ')
        print o
        fd.write('\noutput : ' + str(o) + '\n')
        fd.write('\nNumber of Correct value : ' + str(ans) + ' / 4\n\n')
        
        #첫 번째와 두 번째 weight수정할 때 중복되는 값 저장
        repeated = []
        #두 번째 weight업데이트
        for i in range(4):
            repeated.append((answerLabel[i] - o[i])*o[i]*(1-o[i]))
            for j in range(3):
                weight2[j] = weight2[j] + rho2*repeated[i]*h[j][i]
        
        #첫 번재 weight업데이트
        for i in range(4):#데이터 
            for j in range(3):#한 데이터 안의 순서
                for k in range(2):#1 layer 퍼셉트론
                    for l in range(3):#2 layer 퍼셉트론
                        reSum = repeated[i]*weight2[k+1]
                        weight1[j][k] = weight1[j][k] + rho1*reSum*h[k+1][i]*(1-h[k+1][i])*trainData[j][i]
        #모두 정답이면 학습 종료
        if ans == 4:
            break
        epoch += 1  #epoch증가
        
    fd.close()      #파일 닫기
    
    print 'learning finished'
    
    #테스트 결과 저장할 파일 쓰기모드로 열기
    fd = open('test_output.txt', 'w')
    #테스트데이터와 학습된 weight1값으로 계산 후 바이어스 추가하여 result1배열 생성
    tempResult1 = sigmoid(np.dot(weight1.T, testData))    
    result1 = np.zeros((3, 4))
    result1[0] = [1, 1, 1, 1]
    result1[1] = tempResult1[0]
    result1[2] = tempResult1[1]
    
    #result1배열과 학습된 weight2를 이용하여 최종 아웃풋 계산
    tempResult2 = sigmoid(np.dot(weight2.T, result1))
    
    resultAns = 0   #맞은 개수 저장
    
    #각각의 테스트 샘플이 맞을경우와 안맞을 경우 처리
    for i in range(4):
        if abs(tempResult2[i] - answerLabel[i]) < 0.2:
            resultAns += 1
            print '(', testData[1][i], ', ', testData[2][i], ') ===> XOR Result : ', answerLabel[i], '(learning success) '
            fd.write('(' + str(testData[1][i]) + ', ' + str(testData[2][i]) + ') ===> XOR Result : ' + str(answerLabel[i]) +'(learning success)\n')
        else:
            print '(', testData[1][i], ', ', testData[2][i], ') ===> XOR Result : ', abs(answerLabel[i]-1), '(learning success) '
            fd.write('(' + str(testData[1][i]) + ', ' + str(testData[2][i]) + ') ===> XOR Result : ' + str(abs(answerLabel[i]-1)) +'(learning failure)\n')
    #다 맞을 경우
    if resultAns == 4:
        print 'learning success'
        fd.write('error Rate : 0%')
    #하나라도 틀릴 경우
    else:
        print 'learning failure'
        
    fd.close()     #파일 닫기
        
        
        