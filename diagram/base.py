class BaseDiagram(object):
    def __init__(self, processor, sourceFile, targetFile, text):
        self.proc = processor
        self.text = text
        self.sourceFile = sourceFile
        self.targetFile = targetFile
        self.file = None

    def open(self):
        if self.targetFile is None:
            self.file = NamedTemporaryFile(prefix=self.sourceFile, suffix='png', delete=False)
            sele.file = self.sourceFile + ".png"
        else:
            self.file = open(self.targetFile, 'w')

    def generate(self):
        raise NotImplementedError('abstract base class is abstract')


class BaseProcessor(object):
    DIAGRAM_CLASS = None
    CHARSET = None
    CHECK_ON_STARTUP = True

    def load(self):
        raise NotImplementedError('abstract base class is abstract')

    def extract_blocks(self, view):
        raise NotImplementedError('abstract base class is abstract')

    def process(self, sourceFile, text_blocks):
        diagrams = []
        for block in text_blocks:
            try:
                print("Rendering diagram for block: %r" % block)
                diagram = self.DIAGRAM_CLASS(self, sourceFile, None, block)
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
