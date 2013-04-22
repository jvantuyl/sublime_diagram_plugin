from sublime_plugin import TextCommand
from sublime import error_message
from .diagram import setup, process


class DisplayDiagrams(TextCommand):
    def run(self, edit):
        print("Processing diagrams in %r..." % self.view)
        if not process(self.view):
            error_message("No diagrams overlap selections.\n\n" \
                "Nothing to process.")

    def isEnabled(self):
        return True

try:
    setup()
except Exception:
    error_message("Unable to load diagram plugin, check console for details.")
    raise
