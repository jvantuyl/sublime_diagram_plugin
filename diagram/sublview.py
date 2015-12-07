from .base import BaseViewer
import sys
from subprocess import check_call, Popen as run_command


class SublViewer(BaseViewer):
    def load(self):
        if not check_call("which subl > /dev/null", shell=True) == 0:
            raise Exception("Can't find subl")

    def view(self, diagram_files):
        displaycmd = ['subl']
        displaycmd.extend(diagram_file.name for diagram_file in diagram_files)
        run_command(displaycmd).wait()
