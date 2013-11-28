from .base import BaseViewer
from subprocess import check_call, Popen as execute

class OSDefaultViewer(BaseViewer):
	def load(self):
		print("  *  " + __name__ + " loaded")

	def view(self, diagram_files):
		for f in diagram_files:
			execute("explorer \"" + f.name + "\"")

		# displaycmd.extend(diagram_file.name for diagram_file in diagram_files)
		# run_command(displaycmd).wait()
