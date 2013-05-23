from .base import BaseViewer
import sys
from subprocess import check_call, Popen as run_command


class FreedesktopDefaultViewer(BaseViewer):
    def load(self):
        if not check_call("which xdg-open > /dev/null", shell=True) == 0:
            raise Exception("Freedesktop-conforming default application not found!")

    def view(self, diagram_files):
        displaycmd = ['xdg-open']
        displaycmd.extend(diagram_file.name for diagram_file in diagram_files)
        run_command(displaycmd).wait()
