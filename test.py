class A:
    def __init__(self):
        self.__list=[]
    @property
    def event(self):
        return self.__list
    @event.setter
    def event(self,value):
        self.__list=value

a=A()
print(a.event)