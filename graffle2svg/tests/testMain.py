
from unittest import makeSuite, TestCase, TestSuite
from mock import Mock,  patch
from main import TargetSvg,  GraffleParser,  GraffleInterpreter
import xml.dom.minidom

class TestMkHex(TestCase):
    def setUp(self):
        self.gi =TargetSvg()

    def testZero(self):
        self.assertEqual(self.gi.mkHex(0.0),"00")

    def testFull(self):
        self.assertEqual(self.gi.mkHex(1.0) , "ff")

    def testOne(self):
        self.assertEqual(self.gi.mkHex(1.0/255) , "01")

    def testFifteen(self):
        self.assertEqual(self.gi.mkHex(15.0/255) , "0f")

    def test254(self):
        self.assertEqual(self.gi.mkHex(254.0/255) , "fe")

class TestGraffleParser(TestCase):
    def setUp(self):
        self.gp = GraffleParser()
    
    def tearDown(self):
        del self.gp

    def testGraffleDictInteger(self):
        p = xml.dom.minidom.parseString("<dict><key>ImageCounter</key><integer>1</integer></dict>")
        dict = self.gp.ReturnGraffleDict(p.firstChild)
        self.assertEqual(dict['ImageCounter'], '1')
 
    def testGraffleDictReal(self):
        p = xml.dom.minidom.parseString("<dict><key>Size</key><real>19</real></dict>")
        dict = self.gp.ReturnGraffleDict(p.firstChild)
        self.assertEqual(dict['Size'], '19')

    def testGraffleDictReal(self):
        p = xml.dom.minidom.parseString("<dict><key>Shape</key><string>RoundRect</string></dict>")
        dict = self.gp.ReturnGraffleDict(p.firstChild)
        self.assertEqual(dict['Shape'], 'RoundRect')

class scope(dict):
    def __init__(self):
        self.appendScope=Mock()
        self.popScope=Mock()
        dict.__init__(self)

class TestGraffleInterpreterBoundingBox(TestCase):
    def setUp(self):
        self.gi = GraffleInterpreter()
        self.MockTarget = Mock()
        self.MockTarget.style=scope()
        self.gi.setTarget(self.MockTarget)
        
    def tearDown(self):
        del self.MockTarget
        del self.gi

    @patch('geom.out_of_boundingbox')
    def testTextWithCoordinatesOutOfBoundinBoxShouldNotAddToTarget(self, mockBounds):
        self.gi.bounding_box = ((-1, -1),  (1,  1))
        mockBounds.return_value = True
        self.gi.itterateGraffleGraphics([{'Class':'ShapedGraphic', 'Bounds':'{{0, 0}, {756, 553}}','Shape':'RoundRect', 'ID':5, 'Text':{'Text':'test'}}])
        self.assertFalse(any([ mthd_call[0]=='addText' for mthd_call in self.MockTarget.method_calls]))

    @patch('geom.out_of_boundingbox')
    def testShapedGraphicWithCoordinatesOutOfBoundinBoxShouldNotAddToTarget(self, mockBounds):
        self.gi.bounding_box = ((-1, -1),  (1,  1))
        mockBounds.return_value = True
        self.gi.itterateGraffleGraphics([{'Class':'ShapedGraphic', 'Bounds':'{{0, 0}, {756, 553}}','Shape':'RoundRect', 'ID':5}])
        self.assertFalse(any([ mthd_call[0]=='addRect' for mthd_call in self.MockTarget.method_calls]))
        
    @patch('geom.out_of_boundingbox')
    def testShapedGraphicWithCoordinatesInBoundingBoxShouldAddToTarget(self, mockBounds):
        self.gi.bounding_box = ((-1, -1),  (1,  1))
        mockBounds.return_value = False
        self.gi.itterateGraffleGraphics([{'Class':'ShapedGraphic', 'Bounds':'{{0, 0}, {756, 553}}','Shape':'RoundRect',  'ID':5}])
        self.assertTrue(any([ mthd_call[0]=='addRect' for mthd_call in self.MockTarget.method_calls]))

    def testShapedGraphicWithNoBoundingBoxShouldAddToTarget(self):
        self.gi.bounding_box=None
        self.gi.itterateGraffleGraphics([{'Class':'ShapedGraphic', 'Bounds':'{{0, 0}, {756, 553}}','Shape':'RoundRect',  'ID':5}])
        self.assertTrue(any([ mthd_call[0]=='addRect' for mthd_call in self.MockTarget.method_calls]))

    @patch('geom.out_of_boundingbox')
    def testLineGraphicWithCoordinatesOutOfBoundinBoxShouldNotAddToTarget(self, mockBounds):
        self.gi.bounding_box = ((-1, -1),  (1,  1))
        mockBounds.return_value = True
        self.gi.itterateGraffleGraphics([{'Class':'LineGraphic', 'Points':['{0, 0}', '{756, 553}'], 'ID':5}])
        self.assertFalse(any([ mthd_call[0]=='addPath' for mthd_call in self.MockTarget.method_calls]))
        
    @patch('geom.out_of_boundingbox')
    def testLineGraphicWithCoordinatesInBoundingBoxShouldAddToTarget(self, mockBounds):
        self.gi.bounding_box = ((-1, -1),  (1,  1))
        mockBounds.return_value = False
        self.gi.itterateGraffleGraphics([{'Class':'LineGraphic', 'Points':['{0, 0}', '{756, 553}'], 'ID':5}])
        self.assertTrue(any([ mthd_call[0]=='addPath' for mthd_call in self.MockTarget.method_calls]))

    def testLineGraphicWithNoBoundingBoxShouldAddToTarget(self):
        self.gi.itterateGraffleGraphics([{'Class':'LineGraphic', 'Points':['{0, 0}', '{756, 553}'], 'ID':5}])
        self.assertTrue(any([ mthd_call[0]=='addPath' for mthd_call in self.MockTarget.method_calls]))


def get_tests():
    TS = TestSuite()
    TS.addTest(makeSuite(TestMkHex))
    TS.addTest(makeSuite(TestGraffleParser))
    TS.addTest(makeSuite(TestGraffleInterpreterBoundingBox))
    return TS
