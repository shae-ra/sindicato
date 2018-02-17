import unittest

class FixturesTest(unittest.TestCase):

    def setUp(self):
        print('In setUp()')
        self.fixture = [84625731,
        12949573,
        'activo',
        84612357462,
        'Ramirez',
        'Edmundo',
        '22-06-1990',
        28,
        'soltero',
        'argentino',
        'Azcuenaga',
        425,
        '3ro',
        '4',
        '1523',
        'Torcuato',
        'Torcuato',
        '(0220) 4624-4542',
        '(011) 15529392',
        'ramed90@hotmail.com.ar']

    def tearDown(self):
        print('In tearDown()')
        del self.fixture

    def test(self):
        print('in test()')
        

if __name__ == '__main__':
    unittest.main()
