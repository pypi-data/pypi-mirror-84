from cas.models import BuildEnvironment

import os
import sys
import subprocess
import hashlib
import logging
from typing import List, Dict
from pathlib import Path

class BaseCompiler():
    """
    Base compiler class from which all compilers should extend.
    """
    def __init__(self, env: BuildEnvironment, config: dict):
        self._env = env
        self._config = config

    def clean(self):
        """
        Removes all output files of the project.
        """
        raise NotImplementedError()

    def configure(self):
        """
        Generates the necessary files to build the project.
        """
        return NotImplementedError()

    def build(self):
        """
        Compiles the project.
        """
        raise NotImplementedError()
