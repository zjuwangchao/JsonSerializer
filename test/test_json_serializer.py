#!/usr/bin/env python
#coding=gbk

import platform
import unittest
import re
import add_path
from json_serializer import FixedTypeList, FixedTypeListException
from json_serializer import load_from_json, dump_to_json


class TestFixedTypeList(unittest.TestCase):
    def setUp(self):
        pass

    def test_insert(self):
        fixed_type_list = FixedTypeList(int)
        fixed_type_list.insert(0, 5)
        self.assertEqual(len(fixed_type_list), 1)

        self.assertRaises(FixedTypeListException, fixed_type_list.insert,
                1, "string")
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


class TestJsonSerializer(unittest.TestCase):
    class _B:
        def __init__(self):
            self.ba = 0

    class _A:
        def __init__(self):
            self.a = 0
            self.b = False
            self.c = TestJsonSerializer._B()
            self.d = FixedTypeList(int)

    class _C:
        def __init__(self):
            self.ca = 0
            self.cb = TestJsonSerializer._B()
            self.cc = ""

    class _D:
        def __init__(self):
            self.a = False
            self.b = FixedTypeList(TestJsonSerializer._B)
            self.c = TestJsonSerializer._C()

    def setUp(self):
        pass

    def test_load_and_dump(self):
        a = load_from_json(TestJsonSerializer._A(), '{"a":5, "b":true, "c":{"ba":6}, "d":[0,1,2,3]}')
        self.assertEqual(a.a, 5)
        self.assertEqual(a.b, True)
        self.assertEqual(a.c.ba, 6)
        self.assertEqual(a.d, [0, 1, 2, 3])

        dump_str = dump_to_json(a, no_extra_space=False)
        expect_json_str = '{"a": 5, "c": {"ba": 6}, '\
                '"b": true, "d": [0, 1, 2, 3]}'
        self.assertEqual(dump_str, expect_json_str)

        dump_str = dump_to_json(a, no_extra_space=True)
        expect_json_str = '{"a":5,"c":{"ba":6},"b":true,"d":[0,1,2,3]}'
        self.assertEqual(dump_str, expect_json_str)

        input_json = '{"a":true, "b":[{"ba":10}, {"ba":20}], '\
                '"c":{"ca":1, "cc":"test str", "cb":{"ba":50}}}'
        d = load_from_json(TestJsonSerializer._D(), input_json)
        self.assertEqual(d.a, True)
        self.assertEqual(len(d.b), 2)
        self.assertEqual(d.b[0].ba, 10)
        self.assertEqual(d.b[1].ba, 20)
        self.assertEqual(d.c.ca, 1)
        self.assertEqual(d.c.cb.ba, 50)
        self.assertEqual(d.c.cc, "test str")

        dump_str = dump_to_json(d)
        expect_json_str = '{"a":true,"c":{"cc":"test str",'\
                '"cb":{"ba":50},"ca":1},"b":[{"ba":10},{"ba":20}]}'
        self.assertEqual(dump_str, expect_json_str)

    class _E:
        def __init__(self):
            self.a = []

    def assertRaisesRegexpWrapper(self, exception, regexp, callable, *args, **kwds):
        if platform.python_version() >= "2.7":
            self.assertRaisesRegexp(exception, regexp, callable, *args, **kwds)
        else:
            try:
                callable(*args, **kwds)
                self.assertTrue(False, "don't raise exception %s" % (type(exception)))
            except exception, e:
                self.assertNotEqual(re.search(regexp, str(e)), None)

    def test_load_error(self):
        self.assertRaisesRegexpWrapper(ValueError,
                "must use FixedTypeList to store json array",
                load_from_json, TestJsonSerializer._E(), '{"a":[1,2]}')
        self.assertRaisesRegexpWrapper(ValueError, ".*has no attribute\[b\]",
                load_from_json, TestJsonSerializer._E(), '{"b":[1,2]}')

    def test_encoding(self):
        c = load_from_json(TestJsonSerializer._C(), '{"ca":10, "cb":{"ba":20}, "cc":"中文"}')
        self.assertEqual(c.cc, u'中文')

        expect_json_str = '{"cc":"中文","cb":{"ba":20},"ca":10}'
        self.assertEqual(dump_to_json(c), expect_json_str)

if __name__ == '__main__':
    unittest.main()
