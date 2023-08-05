import unittest
from ranjg import genstr

class TestGenstr(unittest.TestCase):

    def test_genstr_with_empty_schema(self):
        schema = {}
        generated = genstr(schema)
        self.assertIsInstance(generated, str)
        self.assertTrue(generated.isalpha())

    def test_genstr_with_maxLength_0(self):
        schema = {"maxLength": 0}
        self.assertEqual(genstr(schema), "")

    def test_genstr_with_minLength(self):
        schema = {"minLength": 100}
        generated = genstr(schema)
        self.assertIsInstance(generated, str)
        self.assertGreaterEqual(len(generated), 100)

    def test_genstr_with_length(self):
        schema = {"minLength": 10, "maxLength": 10}
        generated = genstr(schema)
        self.assertIsInstance(generated, str)
        self.assertEqual(len(generated), 10)
