﻿from __future__ import absolute_import
from .plantuml import PlantUMLProcessor
from .sublime3 import Sublime3Viewer
from .quicklook import QuickLookViewer
from .preview import PreviewViewer
from .eog import EyeOfGnomeViewer
from .freedesktop_default import FreedesktopDefaultViewer
from .windows import WindowsDefaultViewer
from itertools import count
from threading import Thread
from sublime import error_message, load_settings
import sys

INITIALIZED = False
AVAILABLE_PROCESSORS = [PlantUMLProcessor]
AVAILABLE_VIEWERS = [
    Sublime3Viewer,
    QuickLookViewer,
    EyeOfGnomeViewer,
    PreviewViewer,
    FreedesktopDefaultViewer,
    WindowsDefaultViewer,
]
ACTIVE_PROCESSORS = []
ACTIVE_VIEWER = None

def setup():
    global INITIALIZED
    global ACTIVE_PROCESSORS
    global ACTIVE_VIEWER

    ACTIVE_PROCESSORS = []
    ACTIVE_VIEWER = None

    sublime_settings = load_settings("Diagram.sublime-settings")
    print("Viewer Setting: " + sublime_settings.get("viewer"))

    for processor in AVAILABLE_PROCESSORS:
        try:
            print("Loading processor class: %r" % processor)
            proc = processor()
            proc.CHARSET = sublime_settings.get('charset', None)
            proc.CHECK_ON_STARTUP = sublime_settings.get('check_on_startup', True)
            proc.NEW_FILE = sublime_settings.get('new_file', True)
            proc.OUTPUT_FORMAT = sublime_settings.get('output_format', 'png')
            proc.load()
            ACTIVE_PROCESSORS.append(proc)
            print("Loaded processor: %r" % proc)
        except Exception:
            print("Unable to load processor: %r" % processor)
            sys.excepthook(*sys.exc_info())
    if not ACTIVE_PROCESSORS:
        raise Exception('No working processors found!')

    for viewer in AVAILABLE_VIEWERS:
        if viewer.__name__.find(sublime_settings.get("viewer")) != -1:
            try:
                print("Loading viewer class from configuration: %r" % viewer)
                vwr = viewer()
                vwr.load()
                ACTIVE_VIEWER = vwr
                print("Loaded viewer: %r" % vwr)
                break
            except Exception:
                print("Unable to load configured viewer, falling back to autodetection...")
                sys.excepthook(*sys.exc_info())

    if ACTIVE_VIEWER is None:
        for viewer in AVAILABLE_VIEWERS:
            print("Trying Viewer " + viewer.__name__)
            try:
                print("Loading viewer class: %r" % viewer)
                vwr = viewer()
                vwr.load()
                ACTIVE_VIEWER = vwr
                print("Loaded viewer: %r" % vwr)
                break
            except Exception:
                print("Unable to load viewer: %r" % viewer)
                sys.excepthook(*sys.exc_info())

    if ACTIVE_VIEWER is None:
        raise Exception('No working viewers found!')

    INITIALIZED = True
    print("Processors: %r" % ACTIVE_PROCESSORS)
    print("Viewer: %r" % ACTIVE_VIEWER)


def process(view):
    diagrams = []

    for processor in ACTIVE_PROCESSORS:
        blocks = []

        for block in processor.extract_blocks(view):
            add = False
            for sel in view.sel():
                if sel.intersects(block):
                    add = True
                    break
            else:  # if there are no selections, add all blocks
                add = True
            if add:
                blocks.append(view.substr(block))

        if blocks:
            diagrams.append((processor, blocks, ))

    if diagrams:
        sourceFile = view.file_name()
        t = Thread(target=render_and_view, args=(sourceFile, diagrams,))
        t.daemon = True
        t.start()
        return True
    else:
        return False


def render_and_view(sourceFile, diagrams):
    print("[DIAGRAM] Rendering: %r" % diagrams)
    sequence_counter = count()
    diagram_files = []

    for processor, blocks in diagrams:
        diagram_files.extend(processor.process(sourceFile, blocks, sequence_counter))

    if diagram_files:
        for (is_success, status_message, file) in diagram_files:
            if is_success:
                print("[DIAGRAM] %r viewing %r" % (ACTIVE_VIEWER, file))
                ACTIVE_VIEWER.view([file])
            else:
                error_message(status_message)
    else:
        error_message("No diagrams generated...")
