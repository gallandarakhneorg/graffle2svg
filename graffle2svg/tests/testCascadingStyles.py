#!/usr/bin/env python3

from unittest import makeSuite, TestCase, TestSuite

from graffle2svg.styles import CascadingStyles

class TestDefaults(TestCase):
    def setUp(self):
        self.cs = CascadingStyles({"font":"arial","font-size":"12pt"})
        
    def testNone(self):
        self.assertEqual(str(self.cs), "")
        
    def testRemoveScope(self):
        self.cs.appendScope()
        self.cs["font"] = "newfont"
        self.cs.popScope()
        self.assertEqual(str(self.cs), "")
        
        
    def testIgnoreDefault(self):
        self.cs.appendScope()
        self.cs["font"] = "newfont"
        self.cs.appendScope()
        self.cs["font"] = "arial"
        self.assertEqual(str(self.cs), "")
        
        
class TestScope(TestCase):
    def setUp(self):
        self.cs = CascadingStyles({"font":"arial","font-size":"12pt"})
        
    def testRemoveScope(self):
        self.cs.appendScope()
        self.cs["font"] = "newfont"
        self.cs["font"] == "newfont"

def get_tests():
    TS = TestSuite()
    TS.addTest(makeSuite(TestDefaults))
    TS.addTest(makeSuite(TestScope))
    return TS
