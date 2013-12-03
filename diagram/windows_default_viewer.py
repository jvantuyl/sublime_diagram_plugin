from .base import BaseViewer
from os import startfile as execute
from sys import platform

class WindowsDefaultViewer(BaseViewer):
    def load(self):
        if platform not in ('win32',):
            raise Exception("Currently only supported on Windows")

    def view(self, diagram_files):
        for f in diagram_files:
            execute(f.name)
