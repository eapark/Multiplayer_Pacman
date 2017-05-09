class parent():
    def __init__(self):
        self.list = list()
        self.list.append(1)
        self.list.append(2)

class child():
    def __init__(self,pclass):
        self.pclass = pclass
    def dothething(self):
        self.pclass.list.remove(1)

if __name__=="__main__":
    p = parent()
    c = child(p)
    c.dothething()
    print p.list

