import sys
import os
from os import path
import random
import shutil
from test.support import captured_stdout
import unittest
from unittest.mock import patch
from ranjg.__main__ import main as module_main

class TestGenMain(unittest.TestCase):

    TEST_TMP_DIR = "./test-tmp/test_gen_main"
    TEST_TMP_DIR_PRE = path.join(TEST_TMP_DIR, f"{random.randint(0,2**64):X}")

    @classmethod
    def setUpClass(cls):
        if path.exists(cls.TEST_TMP_DIR_PRE):
            shutil.rmtree(cls.TEST_TMP_DIR_PRE)
        os.makedirs(cls.TEST_TMP_DIR_PRE, exist_ok=True)

    def test_gen_main_with_schema_file(self):
        schema_file = "./test-resources/schema-legal-type_str.json"

        testargs = ["__main__.py", schema_file]

        with captured_stdout() as stdout:
            with patch.object(sys, 'argv', testargs):
                module_main()
        
        output = stdout.getvalue()

        self.assertTrue(output.startswith("\""))
        self.assertTrue(output.endswith("\""))
        self.assertTrue("\n" not in output)

    def test_gen_main_with_schema_file_and_output_file(self):
        schema_file = "./test-resources/schema-legal-type_str.json"
        output_file = path.join(self.TEST_TMP_DIR_PRE, "test_gen_main_with_schema_file_and_output_file_output.json")

        testargs = ["__main__.py", schema_file, "-j", output_file]

        with captured_stdout() as stdout:
            with patch.object(sys, 'argv', testargs):
                module_main()
        
        output = stdout.getvalue()

        self.assertEqual(output, "")
        self.assertTrue(path.exists(output_file))
