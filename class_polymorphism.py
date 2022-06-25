class Point:
    def __init__(self):
        self.x=int(input('x='))
        self.y=int(input('y='))
    def disp(self):
        pass

class Rect(Point):
    def __init__(self):
        super().__init__()
        self.w=int(input('w='))
        self.h=int(input('h='))
    def disp(self):
        print('사각형', self.x, self.y, self.w, self.h)

class Circle(Point):
    def __init__(self):
        super().__init__()
        self.r=int(input('r='))        
    def disp(self):
        print('원', self.x, self.y, self.r)    

def main():
    li = list()
    while True:
        s=input('1.사각형 2.원 3.조회 4.종료:')
        if s=='1':
            li.append(Rect())
        if s=='2':
            li.append(Circle())
        if s=='3':
            for i in li:
                i.disp()
        if s=='4':
            break
    print('프로그램을 종료합니다')

main()