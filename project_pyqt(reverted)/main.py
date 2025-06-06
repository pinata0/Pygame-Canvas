import os
import sys

current_path = os.path.abspath(__file__)
base_dir = os.path.dirname(current_path)
os.chdir(base_dir)

from gui import app
