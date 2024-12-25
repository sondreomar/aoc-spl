#!/usr/bin/env python
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from splunklib.searchcommands import Configuration, GeneratingCommand, dispatch

INPUTS = Path("../aoc/inputs")


@Configuration(type="reporting", streaming=False)
class InputAOC(GeneratingCommand):
    def generate(self):
        if not self.fieldnames:
            raise ValueError("No filename provided")
        if not re.search(r"^[\w,\s-]+(\.[\w,\s-]+)?$", self.fieldnames[0]):
            raise ValueError("Invalid filename provided")
        path = INPUTS / f"{self.fieldnames[0]}"
        if not path.exists() or not path.is_file():
            raise ValueError("File does not exist")
        with open(path) as f:
            for line in f:
                yield {"_raw": line.strip()}


dispatch(InputAOC, sys.argv, sys.stdin, sys.stdout, __name__)
