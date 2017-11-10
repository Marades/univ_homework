#파일을 읽기모드로 열어 글자를 읽어들이고 저장한 후 닫는다
fd = open('input_data.txt', 'r')
lines = fd.readlines()
fd.close()

#빈 배열을 하나 생성한 후 파일에서 읽어들인 글자를 공백 기준으로 나누어 저장한다
arr = []
for line in lines:
    arr.append(line.split())
       
#파일을 쓰기 모드로 열어 arr에 담긴 정보를 분류하여 저장한 후 닫는다
fd = open('output_result.txt', 'w')
for a in arr:
    if (int)(a[0]) < 85 and (int)(a[1]) > 10:
        fd.write('body: ' + a[0] + ' tail: ' + a[1] + ' ==> ' + 'salmon\n')
    else:
        fd.write('body: ' + a[0] + ' tail: ' + a[1] + ' ==> ' + 'seabass\n')
fd.close()