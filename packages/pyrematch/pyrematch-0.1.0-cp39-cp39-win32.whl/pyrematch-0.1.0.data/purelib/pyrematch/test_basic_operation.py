import unittest
from . import rematch as re

class Test(unittest.TestCase):

    def setUp(self):
        # Aquí, opcionalmente, ejecuta lo que deberías ejecutar antes
        # de comenzar cada test.
        string = "one two three four five ..."
        pattern = ".*!x{one} !y{two} !z{three}.*"
        self.regex_obj = re.compile(pattern)
        self.match_obj = self.regex_obj.find(string)

    #MatchObject tests

    def test_start(self):
        self.assertEqual(self.match_obj.start('x'), 0)
        self.assertEqual(self.match_obj.start('y'), 4)
        self.assertEqual(self.match_obj.start('z'), 8)

    def test_end(self):
        self.assertEqual(self.match_obj.end('x'), 3)
        self.assertEqual(self.match_obj.end('y'), 7)
        self.assertEqual(self.match_obj.end('z'), 13)

    def test_span(self):
        self.assertTupleEqual(self.match_obj.span('x'), (0, 3))
        self.assertTupleEqual(self.match_obj.span('y'), (4, 7))
        self.assertTupleEqual(self.match_obj.span('z'), (8, 13))
    '''
    def test_group(self):
        self.assertEqual(self.match_obj.group('x'), 'one')
        self.assertEqual(self.match_obj.group(1), 'one')
        self.assertEqual(self.match_obj.group('y'), 'two')
        self.assertEqual(self.match_obj.group(2), 'two')
        self.assertEqual(self.match_obj.group('z'), 'three')
        self.assertEqual(self.match_obj.group(3), 'three')

    def test_gruops(self): #Agregar el group(0) cuando esté definida la sintaxis
        self.assertTupleEqual(self.match_obj.groups(), ('x', 'y', 'z'))

    def test_groupdict(self):
        self.assertDictEqual(self.match_obj.groupdict(), {'x': 'one', 'y': 'two', 'z': 'three'})


    #RegexObject tests

    def test_find(self):
        regex_obj = re.compile('.*!x{a...s}.*')
        #match = regex_obj.find("abcdefgh")
        #self.assertIsNone(match)
        match = regex_obj.find("abyssal")
        self.assertIsNotNone(match)
        self.assertEqual(match.start('x'), 0)
        self.assertEqual(match.end('x'), 5)
        self.assertTupleEqual(match.span('x'), (0, 5))
        #self.assertEqual(match.group('x'), 'abyss')
        #self.assertTupleEqual(match.groups(), ('x'))
        #self.assertDictEqual(match.groupdict(), {'x': 'abyss'})

    '''
    def test_findall(self):
        regex_obj = re.compile('.*!x{teen}.*')
        matches = regex_obj.findall('abcdefgh')
        self.assertListEqual(matches, [])
        matches = regex_obj.findall('fifteen, sixteen, seventeen,...')
        expected = [(3, 7), (12, 16), (23, 27)]
        for pos in range(len(matches)):
            match = matches[pos]
            self.assertIsNotNone(match)
            self.assertEqual(match.start('x'), expected[pos][0])
            self.assertEqual(match.end('x'), expected[pos][1])
            self.assertTupleEqual(match.span('x'), expected[pos])
            #self.assertEqual(match.group('x'), 'teen')
            #self.assertTupleEqual(match.groups(), ('x'))
            #self.assertDictEqual(match.groupdict(), {'x': 'teen'})

    def test_finditer(self):
        regex_obj = re.compile('.*!x{teen}.*')
        matches_iterator = regex_obj.finditer('fifteen, sixteen, seventeen,...')
        matches = []
        for match in matches_iterator:
            matches.append(match)
        expected = [(3, 7), (12, 16), (23, 27)]
        for pos in range(len(matches)):
            match = matches[pos]
            self.assertIsNotNone(match)
            self.assertEqual(match.start('x'), expected[pos][0])
            self.assertEqual(match.end('x'), expected[pos][1])
            self.assertTupleEqual(match.span('x'), expected[pos])
            #self.assertEqual(match.group('x'), 'teen')
            #self.assertTupleEqual(match.groups(), ('x'))
            #self.assertDictEqual(match.groupdict(), {'x': 'teen'})
    '''
    def test_search(self):
        regex_obj = re.compile('.*!x{a...s}.*')
        match = regex_obj.find("abcdefgh")
        self.assertIsNone(match)
        match = regex_obj.search("abyssal")
        self.assertIsNotNone(match)
        self.assertEqual(match.start('x'), 0)
        self.assertEqual(match.end('x'), 4)
        self.assertTupleEqual(match.span('x'), (0, 4))
        self.assertEqual(match.group('x'), 'abyss')
        self.assertTupleEqual(match.groups(), ('x'))
        self.assertDictEqual(match.groupdict(), {'x': 'abyss'})

    def test_match(self):
        regex_obj = re.compile('.*!x{a...s}.*')
        match = regex_obj.match('the abyssal')
        self.assertIsNone(match)
        match = regex_obj.match('abyssal')
        self.assertIsNotNone(match)
        self.assertEqual(match.start('x'), 0)
        self.assertEqual(match.end('x'), 4)
        self.assertTupleEqual(match.span('x'), (0, 4))
        self.assertEqual(match.group('x'), 'abyss')
        self.assertTupleEqual(match.groups(), ('x'))
        self.assertDictEqual(match.groupdict(), {'x': 'abyss'})


    def test_fullmatch(self):
        regex_obj = re.compile('.*!x{a...s}.*')
        match = regex_obj.fullmatch('abyssal')
        self.assertIsNone(match)
        match = regex_obj.fullmatch('abyss')
        self.assertIsNotNone(match)
        self.assertEqual(match.start('x'), 0)
        self.assertEqual(match.end('x'), 4)
        self.assertTupleEqual(match.span('x'), (0, 4))
        #self.assertEqual(match.group('x'), 'abyss')
        #self.assertTupleEqual(match.groups(), ('x'))
        #self.assertDictEqual(match.groupdict(), {'x': 'abyss'})
    '''
if __name__ == '__main__':
    unittest.main()