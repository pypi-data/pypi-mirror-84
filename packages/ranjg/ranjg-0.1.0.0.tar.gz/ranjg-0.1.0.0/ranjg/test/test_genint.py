import unittest
from ranjg import genint

class TestGenint(unittest.TestCase):

    def test_genint_with_empty_schema(self):
        schema = {}
        self.assertIsInstance(genint(schema), int)

    def test_genint_with_tight_min_max(self):
        schema = {
            "minimum": 5,
            "maximum": 5,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_min_exMax(self):
        schema = {
            "minimum": 5,
            "exclusiveMaximum": 6,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_exMin_max(self):
        schema = {
            "exclusiveMinimum": 4,
            "maximum": 5,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_exMin_exMax(self):
        schema = {
            "exclusiveMinimum": 4,
            "exclusiveMaximum": 6,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_min_max_exMinTrue(self):
        schema = {
            "minimum": 4,
            "exclusiveMinimum": True,
            "maximum": 5,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)

    def test_genint_with_tight_min_max_exMaxTrue(self):
        schema = {
            "minimum": 5,
            "maximum": 6,
            "exclusiveMaximum": True,
        }
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
        self.assertEqual(genint(schema), 5)
