from .base import BaseViewer
import sublime

class Sublime3Viewer(BaseViewer):
	def load(self):
		if not sublime.version().startswith('3'):
			raise Exception("Not Sublime 3!")

	def view(self,diagram_files):
		for diagram_file in diagram_files:
			sublime.active_window().run_command("set_layout",{"cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0], "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]})
			sublime.active_window().focus_group(1)
			sublime.active_window().open_file(diagram_file.name)
