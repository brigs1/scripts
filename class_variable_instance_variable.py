class Person:
    li = []
    def __init__(self, sp):
        #self.li=[]   # 인스턴스 변수는 인스턴스 각각을 관리한다.
        Person.li.append(sp)

    def disp(self):
        print(Person.li)

p1=Person('우유')
p1.disp()
p2=Person('콜라')
p2.disp()
p3=Person('주스')
p3.disp()
