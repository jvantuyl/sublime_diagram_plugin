from .base import BaseViewer
import sublime

class Sublime3Viewer(BaseViewer):
	def load(self):
		if not sublime.version().startswith('3'):
			raise Exception("Not Sublime 3!")

	def view(self,diagram_files):
		for diagram_file in diagram_files:
			sublime.active_window().open_file(diagram_file.name)