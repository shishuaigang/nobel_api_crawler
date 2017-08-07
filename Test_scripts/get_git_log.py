# -*- coding: utf-8 -*-
import os
import subprocess


def gitlog():
    os.chdir(os.path.dirname(os.getcwd()))
    return subprocess.check_output("git log --oneline -1")
