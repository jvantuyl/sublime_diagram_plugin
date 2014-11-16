from .base import BaseViewer
from platform import system

try:
    from os import startfile as execute
except ImportError:
    def execute(*args, **kwargs):
        raise Exception('unable to import os.startfile')


class WindowsDefaultViewer(BaseViewer):
    def load(self):
        if system() != 'Windows':
            raise Exception(
                "WindowsViewer only supported on Windows platforms"
            )

    def view(self, diagram_files):
        for f in diagram_files:
            execute(f.name)
