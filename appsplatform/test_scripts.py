import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from os import path

PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PROJECT_ROOT)
print(BASE_DIR)
print(path.dirname(path.abspath(path.dirname(__file__))))