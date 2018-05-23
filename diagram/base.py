class BaseDiagram(object):
    def __init__(self, processor, sourceFile, text):
        self.proc = processor
        self.text = text
        self.sourceFile = sourceFile

    # returns tuple: (is_success, status_message, file)
    def generate(self):
        raise NotImplementedError('abstract base class is abstract')


class BaseProcessor(object):
    DIAGRAM_CLASS = None
    CHARSET = None
    CHECK_ON_STARTUP = True
    NEW_FILE = False

    def load(self):
        raise NotImplementedError('abstract base class is abstract')

    def extract_blocks(self, view):
        raise NotImplementedError('abstract base class is abstract')

    def process(self, sourceFile, text_blocks, sequence_counter):
        diagrams = []
        for block in text_blocks:
            try:
                sequence = next(sequence_counter)
                print("Rendering diagram for block: %r[%r]" % (block, sequence,))
                diagram = self.DIAGRAM_CLASS(self, sourceFile, block, sequence)
                rendered = diagram.generate()
                diagrams.append(rendered)
            except Exception as e:
                print("Error processing diagram: %r" % e)
                print(repr(block))
        return diagrams


class BaseViewer(object):
    def load(self):
        raise NotImplementedError('abstract base class is abstract')

    def view(self, filenames):
        raise NotImplementedError('abstract base class is abstract')
