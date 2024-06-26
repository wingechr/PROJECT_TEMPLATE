# coding: utf-8
import unittest

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor


class TestNotebooks(unittest.TestCase):
    def run_notebook(self, notebook_path: str):

        with open(notebook_path, "rb") as file:
            nb = nbformat.read(file, nbformat.NO_CONVERT)
        ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
        # TODO: may raise RuntimeWarning: Proactor event loop does not implement ...
        ep.preprocess(nb)

    def test_notebooks(self):
        self.run_notebook("./docs/examples.ipynb")
