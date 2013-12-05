from .base import BaseViewer
from sys import platform

try:
    from os import startfile as execute
except ImportError:
    def execute(*args, **kwargs):
        raise Exception('unable to import os.startfile')


class WindowsDefaultViewer(BaseViewer):
    def load(self):
        if platform not in ('win32',):
            raise Exception("Currently only supported on Windows")

    def view(self, diagram_files):
        for f in diagram_files:
            execute(f.name)
