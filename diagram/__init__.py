from __future__ import absolute_import
from .plantuml import PlantUMLProcessor
from .quicklook import QuickLookViewer
from .preview import PreviewViewer
from .eog import EyeOfGnomeViewer
from threading import Thread
from os.path import splitext
from sublime import error_message, load_settings
import sys

INITIALIZED = False
AVAILABLE_PROCESSORS = [PlantUMLProcessor]
AVAILABLE_VIEWERS = [QuickLookViewer, EyeOfGnomeViewer, PreviewViewer]
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
        if sourceFile is None:
            sourceFile = 'untitled.txt'
        sourceFile = splitext(sourceFile)[0] + '-'
        t = Thread(target=render_and_view, args=(sourceFile, diagrams,))
        t.daemon = True
        t.start()
        return True
    else:
        return False


def render_and_view(sourceFile, diagrams):
    print("Rendering %r" % diagrams)
    diagram_files = []

    for processor, blocks in diagrams:
        diagram_files.extend(processor.process(sourceFile,blocks))

    if diagram_files:
        print("%r viewing %r" % (ACTIVE_VIEWER, [d.name for d in diagram_files]))
        ACTIVE_VIEWER.view(diagram_files)
    else:
        error_message("No diagrams generated...")
