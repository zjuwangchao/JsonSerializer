#!/usr/bin/env python


def add_path(path):
    import sys
    if path not in sys.path:
        sys.path.insert(0, path)

add_path('../src/')


import unittest
from JsonSerializer import FixedTypeList, FixedTypeListException
from JsonSerializer import load_from_json, dump_to_json


class TestFixedTypeList(unittest.TestCase):
    def setUp(self):
        pass

    def test_insert(self):
        fixed_type_list = FixedTypeList(int)
        fixed_type_list.insert(0, 5)
        self.assertEqual(len(fixed_type_list), 1)

        self.assertRaises(FixedTypeListException, fixed_type_list.insert, 1, "string")
        self.assertEqual(len(fixed_type_list), 1)

    def test_append(self):
        fixed_type_list = FixedTypeList(float)
        fixed_type_list.append(5.0)
        fixed_type_list.append(6.0)
        self.assertEqual(len(fixed_type_list), 2)

        self.assertRaises(FixedTypeListException, fixed_type_list.append, 2)
        self.assertEqual(len(fixed_type_list), 2)

    def test_setitem(self):
        fixed_type_list = FixedTypeList(float)
        fixed_type_list.append(5.0)
        try:
            fixed_type_list[0] = "10"
        except FixedTypeListException, e:
            print str(e)
        self.assertEqual(len(fixed_type_list), 1)


class TestLoadFromJson(unittest.TestCase):
    class B:
        def __init__(self):
            self.ba = 0

    class A:
        def __init__(self):
            self.a = 0
            self.b = False
            self.c = TestLoadFromJson.B()
            self.d = FixedTypeList(int)

    class C:
        def __init__(self):
            self.ca = 0
            self.cb = TestLoadFromJson.B()
            self.cc = ""

    class D:
        def __init__(self):
            self.a = False
            self.b = FixedTypeList(TestLoadFromJson.B)
            self.c = TestLoadFromJson.C()

    def setUp(self):
        pass

    def test_load_from_json(self):
        a = TestLoadFromJson.A()
        load_from_json(a, '{"a":5, "b":true, "c":{"ba":6}, "d":[0,1,2,3]}')
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, True)
        self.assertEqual(a.c.ba, 6)
        self.assertEqual(a.d, [0, 1, 2, 3])
        dump_str = dump_to_json(a)
        self.assertEqual(dump_str, '{"a": 5, "c": {"ba": 6}, "b": true, "d": [0, 1, 2, 3]}')

        d = TestLoadFromJson.D()
        load_from_json(d, '{"a":true, "b":[{"ba":10}, {"ba":20}], "c":{"ca":1, "cc":"test str", "cb":{"ba":50}}}')
        self.assertEqual(d.a, True)
        self.assertEqual(len(d.b), 2)
        self.assertEqual(d.b[0].ba, 10)
        self.assertEqual(d.b[1].ba, 20)
        self.assertEqual(d.c.ca, 1)
        self.assertEqual(d.c.cb.ba, 50)
        self.assertEqual(d.c.cc, "test str")

        dump_str = dump_to_json(d)
        self.assertEqual(dump_str, '{"a": true, "c": {"cc": "test str", "cb": {"ba": 50}, "ca": 1}, "b": [{"ba": 10}, {"ba": 20}]}')


if __name__ == '__main__':
    unittest.main()
