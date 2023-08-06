"This module was created for test purpose"


import objname


class Class(objname.AutoName):
    pass


obj_1 = Class()


a = b = objname.AutoName()


c, d = objname.AutoName()


class SubClass(objname.AutoName):
    def __init__(self) -> None:
        super().__init__()


obj_2 = SubClass()


class Numeric:
    def __init__(self, type: object) -> None:
        self.__type__ = type


class Symbol(Numeric, objname.AutoName):
    def __init__(self, type: object) -> None:
        Numeric.__init__(self, type)
        objname.AutoName.__init__(self)


obj_3 = Symbol(complex)


class Atom(objname.AutoName):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return self.name


e, f, g = Atom()


class Namespace:
    attr = objname.AutoName()


for h in [objname.AutoName()]:
    pass


for i, j in [objname.AutoName()]:
    pass
