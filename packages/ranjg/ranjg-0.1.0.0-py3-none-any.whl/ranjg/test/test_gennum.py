import unittest
from ranjg import gennum

class TestGennum(unittest.TestCase):

    def test_gennum_with_empty_schema(self):
        schema = {}
        self.assertIsInstance(gennum(schema), float)

    def test_gennum_with_param_minimum(self):
        schema = {
            "minimum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertGreaterEqual(generated, 1.23)

    def test_gennum_with_param_maximum(self):
        schema = {
            "maximum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertLessEqual(generated, 1.23)

    def test_gennum_with_param_exclusiveMinimum(self):
        schema = {
            "exclusiveMinimum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertGreater(generated, 1.23)

    def test_gennum_with_param_exclusiveMaximum(self):
        schema = {
            "exclusiveMaximum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertLess(generated, 1.23)

    def test_gennum_with_param_minimum_exclusiveMinimum(self):
        schema = {
            "minimum": 1.23E+200,
            "exclusiveMinimum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertGreater(generated, 1.23)

    def test_gennum_with_param_maximum_exclusiveMaximum(self):
        schema = {
            "maximum": 1.23E+200,
            "exclusiveMaximum": 1.23,
        }
        generated = gennum(schema)
        self.assertIsInstance(generated, float)
        self.assertLess(generated, 1.23)

if __name__ == '__main__':
    unittest.main()
