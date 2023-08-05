import os
from os import path
import random
import shutil
import unittest
from ranjg import gen

class TestGen(unittest.TestCase):

    TEST_TMP_DIR = "./test-tmp/test_gen"
    TEST_TMP_DIR_PRE = path.join(TEST_TMP_DIR, f"{random.randint(0,2**64):X}")

    @classmethod
    def setUpClass(cls):
        if path.exists(cls.TEST_TMP_DIR_PRE):
            shutil.rmtree(cls.TEST_TMP_DIR_PRE)
        os.makedirs(cls.TEST_TMP_DIR_PRE, exist_ok=True)

    def test_gen_with_empty_schema(self):
        schema = {}
        gen(schema)

    def test_gen_with_schema_file_path(self):
        gen(schema_file="./test-resources/schema-legal-type_str.json")

    def test_gen_with_output_file_path(self):
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_file_path_output.json")

        gen(schema_file="./test-resources/schema-legal-user_object.json", 
            output_file=output_file)
        
        self.assertTrue(path.exists(output_file))

    def test_gen_with_output_fp(self):
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_with_output_fp_output.json")

        with open(output_file, "w") as fp:
            gen(schema_file="./test-resources/schema-legal-user_object.json", 
                output_fp=fp)
        
        self.assertTrue(path.exists(output_file))


