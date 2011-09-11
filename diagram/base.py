class BaseDiagram(object):
    def __init__(self, processor, text):
        self.proc = processor
        self.text = text

    def generate(self):
        raise NotImplementedError('abstract base class is abstract')


class BaseProcessor(object):
    DIAGRAM_CLASS = None

    def load(self):
        raise NotImplementedError('abstract base class is abstract')

    def extract_blocks(self, view):
        raise NotImplementedError('abstract base class is abstract')

    def process(self, text_blocks):
        diagrams = []
        for block in text_blocks:
            try:
                diagram = self.DIAGRAM_CLASS(self, block)
                rendered = diagram.generate()
                diagrams.append(rendered)
            except Exception, e:
                print "Error processing diagram: %r" % e
                print repr(block)
        return diagrams


class BaseViewer(object):
    def load(self):
        raise NotImplementedError('abstract base class is abstract')

    def view(self, filenames):
        raise NotImplementedError('abstract base class is abstract')
