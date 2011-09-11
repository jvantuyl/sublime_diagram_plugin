from .base import BaseViewer
import sys
from subprocess import check_call


class QuickLookViewer(BaseViewer):
    def load(self):
        assert sys.platform in ('darwin',), "Currently only supported on MacOS"

    def view(self, diagram_files):
        displaycmd = ['qlmanage', '-p']
        displaycmd.extend(diagram_file.name for diagram_file in diagram_files)
        check_call(displaycmd)
