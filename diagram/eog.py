from .base import BaseViewer
import sys
from subprocess import check_call, Popen as run_command


class EyeOfGnomeViewer(BaseViewer):
    def load(self):
        if not check_call("which eog > /dev/null", shell=True) == 0:
            raise Exception("Eye of Gnome not found!")

    def view(self, diagram_files):
        displaycmd = ['eog']
        displaycmd.extend(diagram_file.name for diagram_file in diagram_files)
        run_command(displaycmd).wait()
