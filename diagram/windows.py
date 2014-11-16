from .base import BaseViewer
import sys
import os


class WindowsViewer(BaseViewer):
    def load(self):
        if sys.platform not in ('win32',):
            raise Exception(
                "WindowsViewer only supported on Windows platforms"
            )

    def view(self, diagram_files):
        for diagram_file in diagram_files:
            os.startfile(diagram_file.name)
