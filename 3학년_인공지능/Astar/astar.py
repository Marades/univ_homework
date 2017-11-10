from Tkinter import *
import math

map = []
map.append(range(1, 6))
map.append(range(6, 11))
map.append(range(11, 16))
map.append(range(16, 21))
map.append(range(21, 26))

# 막힌 곳은 0으로 표시
map[0][3] = 0
map[1][1] = 0
map[2][1] = 0
map[1][3] = 0
map[2][3] = 0
map[4][3] = 0

n = 0           #인덱스를 나타낼 변수
times = 0       #실행횟수를 나타낼 변수
G_adder = 0     #g값을 나타내는 변수
nodeName = 11   #목적지 타일 번호를 나타내는 변수

# 노드의 좌표로부터 이름 반환
def getNodeName(location):
    return map[location[0]][location[1]]
    
# 해당 노드로 이동 가능한지 확인
def isExist(location, toVisit, alreadyVisited):
    if location[0] < 0:
        return False
    
    if location[1] < 0:
        return False
    
    if location[0] > 4:
        return False

    if location[1] > 4:
        return False
        
    # 막힌 곳 판정
    if getNodeName(location) == 0:
        return False
        
    # 이미 방문해야 할 목록에 들어있는지 판정
    if location in toVisit:
        return False
        
    # 이미 방문했던 곳 판정
    if location in alreadyVisited:
        return False
        
    return True
    
    
    
# 윈도우 콜백 클래스
class App:
    
    def __init__(self, master):
        # 맵을 그릴 캔버스 생성
        self.canvas = Canvas(master, width = 800, height = 600)
        self.canvas.pack()
        
        # 버튼 생성
        button = Button(master, text = 'run', command = self.run)
        button.pack()
        
        # 맵 그리기
        for row in range(len(map)):
            for col in range(len(map[0])):
                if map[row][col] == 0:
                    fillColor = 'black'
                else:
                    fillColor = 'white'
                    
                self.canvas.create_rectangle(col * 100, row * 100, col * 100 + 100, row * 100 + 100, fill = fillColor, outline = 'blue')
                self.canvas.create_text(col * 100 + 50, row * 100 + 50, text = map[row][col])
        
        # A* 초기화
        start = [2, 0]
        end = [2, 4]
        node = getNodeName(start)
        
        
        self.alreadyVisited = []        #이미 방문한 노드 저장
        self.toVisit = []               #방문해야할 노드 후보 저장
        self.path = []                  #이동 경로 저장
        self.toVisit.append(start)      #방문해야할 노드에 시작점 저장
        
        
        
    
    # A* 알고리즘 반복 수행
    def run(self):

        # 앞으로 방문해야 할 노드가 남아있으면 루프 반복
        if len(self.toVisit) != 0:
            #시작과 끝 노드
            start = [2, 0]
            end = [2, 4]

            #전역변수 명시적으로 불러오기
            global n
            global G_adder
            global times
            global nodeName
            
            #목적지에 도착한 후 run을 눌렀을 시 최종 경로를 콘솔로 출력하며 종료
            if nodeName == getNodeName(end):
                print 'Fianl Path : ',  self.alreadyVisited
                exit()              
       
            # 방문해야 할 노드 목록 중 f값이 가장 작은 노드로 이동
            current = self.toVisit.pop(n)
 
            #g = math.sqrt(pow(abs(current[0] - start[0]), 2) + pow(abs(current[1] - start[1]), 2))
            #h = abs(current[0] - end[0]) + abs(current[1] - end[1])
            #f = g + h
            # 현재 노드 칠하기
            row = current[0]
            col = current[1]
            self.canvas.create_rectangle(col * 100, row * 100, col * 100 + 100, row * 100 + 100, fill = 'red', outline = 'blue')
            
            #현재의 노듭 번호를 가져옴
            nodeName = getNodeName(current)
            
            #목적지 노드에 다다랐을 경우 경로를 gui로 표시
            if nodeName == getNodeName(end):
                for i in range(0, times):
                    item = self.path.pop()
                    tmp = item[3]
                    pathcol = tmp[0]
                    pathrow = tmp[1]
                    self.canvas.create_rectangle(pathrow * 100, pathcol * 100, pathrow * 100 + 100, pathcol * 100 + 100, fill = 'blue', outline = 'red')
                self.canvas.create_rectangle(end[1] * 100, end[0] * 100, end[1] * 100 + 100, end[0] * 100 + 100, fill = 'blue', outline = 'red')
           

            # 현재 노드의 자식 노드(인접 노드)를 방문해야 할 목록에 추가
            childList = []
            childList.append([current[0] - 1, current[1]])
            childList.append([current[0], current[1] + 1])
            childList.append([current[0] + 1, current[1]])
            childList.append([current[0], current[1] - 1])         
            

            
            #탐색횟수 카운팅
            times = times + 1
            #g값보단 h값에 더 크게 영향을 받게 하기 위해 노드 한칸당 증가되는 g값을 0.5로 조정
            G_adder = G_adder + 0.5
            
            #Astar알고리즘에서 필요한 f, g, h 값들을 노드별로 계산하여 넣을 배열 생성
            g = []
            h = []
            f = []
            
            #갈 수 있는 자식노드가 몇번째인지 알기 위해 선언하는 배열 - childList의 몇번째 요소인지를 저장
            seq = []            
            
            #각각의 자식노드에 대하여
            for child in childList:
                # 갈 수 있는 노드인 경우에만 추가
                if isExist(child, self.toVisit, self.alreadyVisited) == True:  
                    child.append(G_adder)       #g값 정보 저장
                    child.append(current)       #부모 노드 저장
                    self.toVisit.append(child)  #방문해야할 노드 리스트에 저장
                    
            #반복문을 돌 때마다 증가하여 인덱스값 찾을 수 있게 해줌
            i = 0
            
            #방분해야할 노드 목록의 f, g, h값 계산하여 배열에 저장
            for node in self.toVisit:
                g.append(node[2])
                h.append(abs(node[0] - end[0]) + abs(node[1] - end[1]))
                f.append(g[i] + h[i])
                i = i + 1           
            
            #f값이 가장 적은 노드의 index저장
            n = f.index(min(f)) 
            
            #OpenList에 방문해야할 노드 목록의 좌표값만 저장
            OpenList = []
            for item in self.toVisit:
                OpenList.append([item[0], item[1]])
            
            
            #A*알고리즘 정보 출력   
            print '0. Try Number : ', times
            print '1. Path : ', self.alreadyVisited
            print '2. Current Position : ', nodeName
            print '3. Open List : ', OpenList
            print '4. g : ', g
            print '5. h : ', h
            print '6. f : ', f
            print ''
            

            #path배열에 인덱스가 n인(f값이 제일 작은) 노드 추가
            self.path.append(self.toVisit[n])
            
            # 이미 방문한 노드에 현재 노드 추가
            self.alreadyVisited.append([current[0], current[1]])
            
            
        
# 메인
root = Tk()
app = App(root)
root.mainloop()
