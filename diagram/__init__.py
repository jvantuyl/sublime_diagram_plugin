from __future__ import absolute_import
from .plantuml import PlantUMLProcessor
from .quicklook import QuickLookViewer
from .eog import EyeOfGnomeViewer
from threading import Thread

INITIALIZED = False
AVAILABLE_PROCESSORS = [PlantUMLProcessor]
AVAILABLE_VIEWERS = [QuickLookViewer, EyeOfGnomeViewer]
ACTIVE_PROCESSORS = []
ACTIVE_VIEWER = None


def setup():
    global INITIALIZED
    global ACTIVE_PROCESSORS
    global ACTIVE_VIEWER

    for processor in AVAILABLE_PROCESSORS:
        try:
            proc = processor()
            proc.load()
            ACTIVE_PROCESSORS.append(proc)
        except Exception:
            print "Unable to load processor: %r" % processor

    for viewer in AVAILABLE_VIEWERS:
        try:
            vwr = viewer()
            vwr.load()
            ACTIVE_VIEWER = vwr
            break
        except Exception:
            print "Unable to load viewer: %r" % viewer
    else:
        raise Exception('No working viewers found!')

    INITIALIZED = True
    print "Processors: %r" % ACTIVE_PROCESSORS
    print "Viewer: %r" % ACTIVE_VIEWER


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
            if add:
                blocks.append(view.substr(block))

        if blocks:
            diagrams.append((processor, blocks, ))

    if diagrams:
        t = Thread(target=render_and_view, args=(diagrams,))
        t.daemon = True
        t.start()
        return True
    else:
        return False


def render_and_view(diagrams):
    print diagrams
    diagram_files = []

    for processor, blocks in diagrams:
        diagram_files.extend(processor.process(blocks))

    if diagram_files:
        ACTIVE_VIEWER.view(diagram_files)

if not INITIALIZED:
    setup()
