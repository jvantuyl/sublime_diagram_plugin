from .base import BaseViewer
import sys
import os
from subprocess import check_call, Popen as run_command


class WindowsViewer(BaseViewer):
    def load(self):
		0
		
    def view(self, diagram_files):
		for diagram_file in diagram_files:
			os.startfile(diagram_file.name)
