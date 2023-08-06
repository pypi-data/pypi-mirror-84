import sys
import unittest

import objname
from . import _module


class LocalVariableSuite(unittest.TestCase):
    def test_object_instance(self) -> None:
        obj = objname.AutoName()
        self.assertTrue(isinstance(obj, objname.AutoName))

    def test_single_assignment(self) -> None:
        obj = objname.AutoName()
        self.assertEqual(obj.name, "obj")

    def test_multiple_assignment(self) -> None:
        a = b = c = objname.AutoName()
        self.assertEqual(a.name, "c")
        self.assertEqual(b.name, "c")
        self.assertEqual(c.name, "c")

    def test_unpacking(self) -> None:
        x, y = objname.AutoName()
        self.assertEqual(x.name, "x")
        self.assertEqual(y.name, "y")

    def test_subclass(self) -> None:
        class SubClass(objname.AutoName):
            def __init__(self) -> None:
                super().__init__()
        obj = SubClass()
        self.assertEqual(obj.name, "obj")

    def test_multiple_inheritance(self) -> None:
        class Numeric:
            def __init__(self, type: object) -> None:
                self.__type__ = type

        class Symbol(Numeric, objname.AutoName):
            def __init__(self, type: object) -> None:
                Numeric.__init__(self, type)
                objname.AutoName.__init__(self)

        x = Symbol(complex)
        self.assertEqual(x.name, "x")
        self.assertEqual(x.__type__, complex)

    def test_assignment_in_a_child_class_method(self) -> None:
        """ Test the stored name in a method of a class that inherit from
        `objname.AutoName`.
        """
        class Atom(objname.AutoName):
            def __init__(self) -> None:
                super().__init__()

            def __repr__(self) -> str:
                return self.name

        a, b, c = Atom()
        self.assertEqual(repr((a, b, c)), "(a, b, c)")

    def test_assigned_name_in_a_namespace(self) -> None:
        class Namespace:
            attr = objname.AutoName()
        self.assertEqual(Namespace.attr.name, "attr")

    def test_assigned_name_in_a_property_method(self) -> None:
        class Number(objname.AutoName):
            @property
            def custom_attribute_name(self) -> str:
                return self.name
        n = Number()
        self.assertEqual(n.custom_attribute_name, "n")

    def test_multiple_assignment_in_namespace(self) -> None:
        class Multiple:
            attr_1 = attr_2 = objname.AutoName()
        self.assertEqual(Multiple.attr_1.name, "attr_2")
        self.assertEqual(Multiple.attr_2.name, "attr_2")

    def test_single_var_in_for_loop(self) -> None:
        for x in [objname.AutoName()]:
            pass
        self.assertEqual(x.name, "x")

    def test_two_vars_in_for_loop(self) -> None:
        for x, y in [objname.AutoName()]:
            pass
        self.assertEqual(x.name, "x")
        self.assertEqual(y.name, "y")

    def test_default_name(self) -> None:
        self.assertEqual(objname.AutoName().name, "<nameless>")

    def test_inside_function(self) -> None:
        def function():
            inner = objname.AutoName()
            return inner
        self.assertEqual(function().name, "inner")

    def test_extended_arg_opcode(self) -> None:
        _000 = objname.AutoName()
        _001 = objname.AutoName()
        _002 = objname.AutoName()
        _003 = objname.AutoName()
        _004 = objname.AutoName()
        _005 = objname.AutoName()
        _006 = objname.AutoName()
        _007 = objname.AutoName()
        _008 = objname.AutoName()
        _009 = objname.AutoName()
        _010 = objname.AutoName()
        _011 = objname.AutoName()
        _012 = objname.AutoName()
        _013 = objname.AutoName()
        _014 = objname.AutoName()
        _015 = objname.AutoName()
        _016 = objname.AutoName()
        _017 = objname.AutoName()
        _018 = objname.AutoName()
        _019 = objname.AutoName()
        _020 = objname.AutoName()
        _021 = objname.AutoName()
        _022 = objname.AutoName()
        _023 = objname.AutoName()
        _024 = objname.AutoName()
        _025 = objname.AutoName()
        _026 = objname.AutoName()
        _027 = objname.AutoName()
        _028 = objname.AutoName()
        _029 = objname.AutoName()
        _030 = objname.AutoName()
        _031 = objname.AutoName()
        _032 = objname.AutoName()
        _033 = objname.AutoName()
        _034 = objname.AutoName()
        _035 = objname.AutoName()
        _036 = objname.AutoName()
        _037 = objname.AutoName()
        _038 = objname.AutoName()
        _039 = objname.AutoName()
        _040 = objname.AutoName()
        _041 = objname.AutoName()
        _042 = objname.AutoName()
        _043 = objname.AutoName()
        _044 = objname.AutoName()
        _045 = objname.AutoName()
        _046 = objname.AutoName()
        _047 = objname.AutoName()
        _048 = objname.AutoName()
        _049 = objname.AutoName()
        _050 = objname.AutoName()
        _051 = objname.AutoName()
        _052 = objname.AutoName()
        _053 = objname.AutoName()
        _054 = objname.AutoName()
        _055 = objname.AutoName()
        _056 = objname.AutoName()
        _057 = objname.AutoName()
        _058 = objname.AutoName()
        _059 = objname.AutoName()
        _060 = objname.AutoName()
        _061 = objname.AutoName()
        _062 = objname.AutoName()
        _063 = objname.AutoName()
        _064 = objname.AutoName()
        _065 = objname.AutoName()
        _066 = objname.AutoName()
        _067 = objname.AutoName()
        _068 = objname.AutoName()
        _069 = objname.AutoName()
        _070 = objname.AutoName()
        _071 = objname.AutoName()
        _072 = objname.AutoName()
        _073 = objname.AutoName()
        _074 = objname.AutoName()
        _075 = objname.AutoName()
        _076 = objname.AutoName()
        _077 = objname.AutoName()
        _078 = objname.AutoName()
        _079 = objname.AutoName()
        _080 = objname.AutoName()
        _081 = objname.AutoName()
        _082 = objname.AutoName()
        _083 = objname.AutoName()
        _084 = objname.AutoName()
        _085 = objname.AutoName()
        _086 = objname.AutoName()
        _087 = objname.AutoName()
        _088 = objname.AutoName()
        _089 = objname.AutoName()
        _090 = objname.AutoName()
        _091 = objname.AutoName()
        _092 = objname.AutoName()
        _093 = objname.AutoName()
        _094 = objname.AutoName()
        _095 = objname.AutoName()
        _096 = objname.AutoName()
        _097 = objname.AutoName()
        _098 = objname.AutoName()
        _099 = objname.AutoName()
        _100 = objname.AutoName()
        _101 = objname.AutoName()
        _102 = objname.AutoName()
        _103 = objname.AutoName()
        _104 = objname.AutoName()
        _105 = objname.AutoName()
        _106 = objname.AutoName()
        _107 = objname.AutoName()
        _108 = objname.AutoName()
        _109 = objname.AutoName()
        _110 = objname.AutoName()
        _111 = objname.AutoName()
        _112 = objname.AutoName()
        _113 = objname.AutoName()
        _114 = objname.AutoName()
        _115 = objname.AutoName()
        _116 = objname.AutoName()
        _117 = objname.AutoName()
        _118 = objname.AutoName()
        _119 = objname.AutoName()
        _120 = objname.AutoName()
        _121 = objname.AutoName()
        _122 = objname.AutoName()
        _123 = objname.AutoName()
        _124 = objname.AutoName()
        _125 = objname.AutoName()
        _126 = objname.AutoName()
        _127 = objname.AutoName()
        _128 = objname.AutoName()
        _129 = objname.AutoName()
        _130 = objname.AutoName()
        _131 = objname.AutoName()
        _132 = objname.AutoName()
        _133 = objname.AutoName()
        _134 = objname.AutoName()
        _135 = objname.AutoName()
        _136 = objname.AutoName()
        _137 = objname.AutoName()
        _138 = objname.AutoName()
        _139 = objname.AutoName()
        _140 = objname.AutoName()
        _141 = objname.AutoName()
        _142 = objname.AutoName()
        _143 = objname.AutoName()
        _144 = objname.AutoName()
        _145 = objname.AutoName()
        _146 = objname.AutoName()
        _147 = objname.AutoName()
        _148 = objname.AutoName()
        _149 = objname.AutoName()
        _150 = objname.AutoName()
        _151 = objname.AutoName()
        _152 = objname.AutoName()
        _153 = objname.AutoName()
        _154 = objname.AutoName()
        _155 = objname.AutoName()
        _156 = objname.AutoName()
        _157 = objname.AutoName()
        _158 = objname.AutoName()
        _159 = objname.AutoName()
        _160 = objname.AutoName()
        _161 = objname.AutoName()
        _162 = objname.AutoName()
        _163 = objname.AutoName()
        _164 = objname.AutoName()
        _165 = objname.AutoName()
        _166 = objname.AutoName()
        _167 = objname.AutoName()
        _168 = objname.AutoName()
        _169 = objname.AutoName()
        _170 = objname.AutoName()
        _171 = objname.AutoName()
        _172 = objname.AutoName()
        _173 = objname.AutoName()
        _174 = objname.AutoName()
        _175 = objname.AutoName()
        _176 = objname.AutoName()
        _177 = objname.AutoName()
        _178 = objname.AutoName()
        _179 = objname.AutoName()
        _180 = objname.AutoName()
        _181 = objname.AutoName()
        _182 = objname.AutoName()
        _183 = objname.AutoName()
        _184 = objname.AutoName()
        _185 = objname.AutoName()
        _186 = objname.AutoName()
        _187 = objname.AutoName()
        _188 = objname.AutoName()
        _189 = objname.AutoName()
        _190 = objname.AutoName()
        _191 = objname.AutoName()
        _192 = objname.AutoName()
        _193 = objname.AutoName()
        _194 = objname.AutoName()
        _195 = objname.AutoName()
        _196 = objname.AutoName()
        _197 = objname.AutoName()
        _198 = objname.AutoName()
        _199 = objname.AutoName()
        _200 = objname.AutoName()
        _201 = objname.AutoName()
        _202 = objname.AutoName()
        _203 = objname.AutoName()
        _204 = objname.AutoName()
        _205 = objname.AutoName()
        _206 = objname.AutoName()
        _207 = objname.AutoName()
        _208 = objname.AutoName()
        _209 = objname.AutoName()
        _210 = objname.AutoName()
        _211 = objname.AutoName()
        _212 = objname.AutoName()
        _213 = objname.AutoName()
        _214 = objname.AutoName()
        _215 = objname.AutoName()
        _216 = objname.AutoName()
        _217 = objname.AutoName()
        _218 = objname.AutoName()
        _219 = objname.AutoName()
        _220 = objname.AutoName()
        _221 = objname.AutoName()
        _222 = objname.AutoName()
        _223 = objname.AutoName()
        _224 = objname.AutoName()
        _225 = objname.AutoName()
        _226 = objname.AutoName()
        _227 = objname.AutoName()
        _228 = objname.AutoName()
        _229 = objname.AutoName()
        _230 = objname.AutoName()
        _231 = objname.AutoName()
        _232 = objname.AutoName()
        _233 = objname.AutoName()
        _234 = objname.AutoName()
        _235 = objname.AutoName()
        _236 = objname.AutoName()
        _237 = objname.AutoName()
        _238 = objname.AutoName()
        _239 = objname.AutoName()
        _240 = objname.AutoName()
        _241 = objname.AutoName()
        _242 = objname.AutoName()
        _243 = objname.AutoName()
        _244 = objname.AutoName()
        _245 = objname.AutoName()
        _246 = objname.AutoName()
        _247 = objname.AutoName()
        _248 = objname.AutoName()
        _249 = objname.AutoName()
        _250 = objname.AutoName()
        _251 = objname.AutoName()
        _252 = objname.AutoName()
        _253 = objname.AutoName()
        _254 = objname.AutoName()
        _255 = objname.AutoName()
        _256 = objname.AutoName()
        self.assertEqual(_256.name, "_256")

    @unittest.skipIf(sys.version_info < (3, 8), "No warlust operator.")
    def test_warlust(self) -> None:
        expression = "\n".join((
            '(x := objname.AutoName())',
            'self.assertEqual(x.name, "x")',
        ))
        exec(expression)

    def test_custom_attribute(self) -> None:
        class Number(objname.AutoName):
            def __init__(self) -> None:
                super().__init__()
                self.name = self.name
        n = Number()
        self.assertEqual(n.name, "n")

    def test_name_collision(self):
        "Test that the name is searched in the correct namespace"
        class Subclass(objname.AutoName):
            def __init__(self):
                interior = objname.AutoName()
                super().__init__()
                self.interior = interior.name

        def namespace():
            exterior = Subclass()
            self.assertEqual(exterior.name, "exterior")
            self.assertEqual(exterior.interior, "interior")
        namespace()

    def test_subclass_arguments(self):
        class Numeric:
            def __init__(self, type: object) -> None:
                self.__type__ = type

        class Variable(objname.AutoName, Numeric):
            def __init__(self, type: object) -> None:
                objname.AutoName.__init__(self)
                Numeric.__init__(self, type)

        foo, var = Variable(int)
        self.assertEqual(foo.name, "foo")
        self.assertEqual(var.name, "var")

    def test_autoname_instance_as_object_attribute(self) -> None:
        class Object:
            def __init__(self):
                self.attribute = objname.AutoName()
        obtained = Object().attribute.name
        self.assertEqual(obtained, "attribute")


class CellVariableSuite(unittest.TestCase):
    def test_single_assignment(self) -> None:
        a = objname.AutoName()
        b = objname.AutoName()
        c = objname.AutoName()

        def inner():
            return a, b, c

        x, y, z = inner()
        self.assertEqual(x.name, "a")
        self.assertEqual(y.name, "b")
        self.assertEqual(z.name, "c")

    def test_multiple_assignment(self) -> None:
        a = b = c = objname.AutoName()

        def inner():
            return a, b, c

        x, y, z = inner()
        self.assertEqual(x.name, "c")
        self.assertEqual(y.name, "c")
        self.assertEqual(z.name, "c")

    def test_unpacking(self) -> None:
        a, b, c = objname.AutoName()

        def inner():
            return a, b, c

        x, y, z = inner()
        self.assertEqual(x.name, "a")
        self.assertEqual(y.name, "b")
        self.assertEqual(z.name, "c")

    def test_subclass(self) -> None:
        class SubClass(objname.AutoName):
            def __init__(self) -> None:
                super().__init__()

        a = SubClass()

        def inner():
            return a

        x = inner()
        self.assertEqual(x.name, "a")

    def test_multiple_inheritance(self) -> None:
        class Numeric:
            def __init__(self, type: object) -> None:
                self.__type__ = type

        class Symbol(Numeric, objname.AutoName):
            def __init__(self, type: object) -> None:
                Numeric.__init__(self, type)
                objname.AutoName.__init__(self)

        x = Symbol(complex)

        def inner():
            return x

        a = inner()
        self.assertEqual(a.name, "x")
        self.assertEqual(a.__type__, complex)

    def test_assignment_in_a_child_class_method(self) -> None:
        class Atom(objname.AutoName):
            def __init__(self) -> None:
                super().__init__()

            def __repr__(self) -> str:
                return self.name

        a, b, c = Atom()

        def inner():
            return a, b, c

        x, y, z = inner()
        self.assertEqual(repr((x, y, z)), "(a, b, c)")

    def test_assigned_name_in_a_property_method(self) -> None:
        class Number(objname.AutoName):
            @property
            def custom_attribute_name(self) -> str:
                return self.name

        n = Number()

        def inner():
            return n

        m = inner()
        self.assertEqual(m.custom_attribute_name, "n")

    def test_single_var_in_for_loop(self) -> None:
        for x in [objname.AutoName()]:
            def inner():
                return x
        a = inner()
        self.assertEqual(a.name, "x")

    def test_two_vars_in_for_loop(self) -> None:
        for x, y in [objname.AutoName()]:
            def inner():
                return x, y
        a, b = inner()
        self.assertEqual(x.name, "x")
        self.assertEqual(y.name, "y")


class ModuleVariableSuite(unittest.TestCase):
    def test_single_assignment(self) -> None:
        self.assertEqual(_module.obj_1.name, "obj_1")

    def test_multiple_assignment(self) -> None:
        self.assertEqual(_module.a.name, "b")
        self.assertEqual(_module.b.name, "b")

    def test_unpacking(self) -> None:
        self.assertEqual(_module.c.name, "c")
        self.assertEqual(_module.d.name, "d")

    def test_subclass(self) -> None:
        self.assertEqual(_module.obj_2.name, "obj_2")

    def test_multiple_inheritance(self) -> None:
        self.assertEqual(_module.obj_3.name, "obj_3")
        self.assertEqual(_module.obj_3.__type__, complex)

    def test_assignment_in_a_child_class_method(self) -> None:
        """ Test the stored name in a method of a class that inherit from
        `objname.AutoName`.
        """
        expected = repr((_module.e, _module.f, _module.g))
        self.assertEqual(expected, "(e, f, g)")

    def test_assigned_name_in_a_namespace(self) -> None:
        self.assertEqual(_module.Namespace.attr.name, "attr")

    def test_single_var_in_for_loop(self) -> None:
        self.assertEqual(_module.h.name, "h")

    def test_two_vars_in_for_loop(self) -> None:
        self.assertEqual(_module.i.name, "i")
        self.assertEqual(_module.j.name, "j")


# Global variables for GlobalVariableSuite
# ========================================


ga = objname.AutoName()
gb = gc = gd = objname.AutoName()
ge, gf = objname.AutoName()


class GSubclass(objname.AutoName):
    def __init__(self) -> None:
        super().__init__()


gg = GSubclass()


class GNumeric:
    def __init__(self, type: object) -> None:
        self.__type__ = type


class GSymbol(GNumeric, objname.AutoName):
    def __init__(self, type: object) -> None:
        GNumeric.__init__(self, type)
        objname.AutoName.__init__(self)


gh = GSymbol(complex)


class GAtom(objname.AutoName):
    def __init__(self) -> None:
        super().__init__()

    def __repr__(self) -> str:
        return self.name


gi, gj, gk = GAtom()


class GNumber(objname.AutoName):
    @property
    def custom_attribute_name(self) -> str:
        return self.name


gl = GNumber()


for gp in [objname.AutoName()]:
    pass


for gq, gr in [objname.AutoName()]:
    pass


class GlobalVariableSuite(unittest.TestCase):
    def test_single_assignment(self) -> None:
        global ga
        self.assertEqual(ga.name, "ga")

    def test_multiple_assignment(self) -> None:
        global gb, gc, gd
        self.assertEqual(gb.name, "gd")
        self.assertEqual(gc.name, "gd")
        self.assertEqual(gd.name, "gd")

    def test_unpacking(self) -> None:
        global ge, gf
        self.assertEqual(ge.name, "ge")
        self.assertEqual(gf.name, "gf")

    def test_subclass(self) -> None:
        global gg
        self.assertEqual(gg.name, "gg")

    def test_multiple_inheritance(self) -> None:
        global gh
        self.assertEqual(gh.name, "gh")
        self.assertEqual(gh.__type__, complex)

    def test_assignment_in_a_child_class_method(self) -> None:
        global gi, gj, gk
        self.assertEqual(repr((gi, gj, gk)), "(gi, gj, gk)")

    def test_assigned_name_in_a_property_method(self) -> None:
        global gl
        self.assertEqual(gl.custom_attribute_name, "gl")

    def test_single_var_in_for_loop(self) -> None:
        global gp
        self.assertEqual(gp.name, "gp")

    def test_two_vars_in_for_loop(self) -> None:
        global gq, gr
        self.assertEqual(gq.name, "gq")
        self.assertEqual(gr.name, "gr")


class IterableUnpackingAndMultipleAssignmentCase(unittest.TestCase):
    def test_0(self) -> None:
        #  6 DUP_TOP
        #  8 STORE_FAST               1 (a)
        # 10 STORE_FAST               2 (b)
        a = b = objname.AutoName()
        self.assertEqual(a.name, "b")
        self.assertEqual(b.name, "b")

    def test_1(self) -> None:
        #  6 UNPACK_SEQUENCE          2
        #  8 STORE_FAST               1 (a)
        # 10 STORE_FAST               2 (b)
        a, b = objname.AutoName()
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")

    def test_2(self) -> None:
        #  6 DUP_TOP
        #  8 STORE_FAST               1 (a)
        # 10 UNPACK_SEQUENCE          2
        # 12 STORE_FAST               2 (b)
        # 14 STORE_FAST               3 (c)
        a = b, c = objname.AutoName()
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")
        self.assertEqual(c.name, "c")

    def test_3(self) -> None:
        #  6 DUP_TOP
        #  8 UNPACK_SEQUENCE          2
        # 10 STORE_FAST               1 (a)
        # 12 STORE_FAST               2 (b)
        # 14 STORE_FAST               3 (c)
        a, b = c = objname.AutoName()
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")
        self.assertEqual(c.name, "c")

    def test_4(self) -> None:
        #  6 DUP_TOP
        #  8 STORE_FAST               1 (a)
        # 10 DUP_TOP
        # 12 STORE_FAST               2 (b)
        # 14 UNPACK_SEQUENCE          2
        # 16 STORE_FAST               3 (c)
        # 18 STORE_FAST               4 (d)
        a = b = c, d = objname.AutoName()
        self.assertEqual(a.name, "b")
        self.assertEqual(b.name, "b")
        self.assertEqual(c.name, "c")
        self.assertEqual(d.name, "d")

    def test_5(self) -> None:
        """ multiple and unpacking
              6 DUP_TOP
              8 UNPACK_SEQUENCE          2
             10 STORE_FAST               1 (a)
             12 STORE_FAST               2 (b)
             14 DUP_TOP
             16 STORE_FAST               3 (c)
             18 STORE_FAST               4 (d)
        """
        a, b = c = d = objname.AutoName()
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")
        self.assertEqual(c.name, "d")
        self.assertEqual(d.name, "d")

    def test_6(self) -> None:
        #  6 DUP_TOP
        #  8 STORE_FAST               1 (a)
        # 10 DUP_TOP
        # 12 STORE_FAST               2 (b)
        # 14 DUP_TOP
        # 16 UNPACK_SEQUENCE          2
        # 18 STORE_FAST               3 (c)
        # 20 STORE_FAST               4 (d)
        # 22 DUP_TOP
        # 24 STORE_FAST               5 (e)
        # 26 STORE_FAST               6 (f)
        a = b = c, d = e = f = objname.AutoName()
        self.assertEqual(a.name, "f")
        self.assertEqual(b.name, "f")
        self.assertEqual(c.name, "c")
        self.assertEqual(d.name, "d")
        self.assertEqual(e.name, "f")
        self.assertEqual(f.name, "f")

    def test_7(self):
        #  6 DUP_TOP
        #  8 UNPACK_SEQUENCE          2
        # 10 STORE_FAST               1 (a)
        # 12 STORE_FAST               2 (b)
        # 14 DUP_TOP
        # 16 STORE_FAST               3 (c)
        # 18 DUP_TOP
        # 20 STORE_FAST               4 (d)
        # 22 UNPACK_SEQUENCE          2
        # 24 STORE_FAST               5 (e)
        # 26 STORE_FAST               6 (f)
        a, b = c = d = e, f = objname.AutoName()
        self.assertEqual(a.name, "a")
        self.assertEqual(b.name, "b")
        self.assertEqual(c.name, "d")
        self.assertEqual(d.name, "d")
        self.assertEqual(e.name, "e")
        self.assertEqual(f.name, "f")


if __name__ == '__main__':

    # A weird bug with global variables can only be tested here
    class TypedObj:
        def __init__(self, type: object) -> None:
            self.__type__ = type

    class NamedObj(TypedObj, objname.AutoName):
        def __init__(self, type: object) -> None:
            TypedObj.__init__(self, type)
            objname.AutoName.__init__(self)

    class ReprObj(objname.AutoName):
        def __repr__(self) -> str:
            return self.name

    class Variable(ReprObj, NamedObj):
        def __init__(self, type: object) -> None:
            ReprObj.__init__(self)
            NamedObj.__init__(self, type)

    foo, var = Variable(int)

    assert foo.name == "foo"
    assert var.name == "var"
    assert foo.__type__ == int
    assert var.__type__ == int

    unittest.main()
