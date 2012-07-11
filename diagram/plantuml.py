from __future__ import absolute_import
from .base import BaseDiagram
from .base import BaseProcessor
from subprocess import Popen as execute, PIPE, STDOUT
from os.path import abspath, dirname, exists, join
from tempfile import NamedTemporaryFile


class PlantUMLDiagram(BaseDiagram):
    def __init__(self, processor, text):
        super(PlantUMLDiagram, self).__init__(processor, text)
        self.file = NamedTemporaryFile(suffix='.png')

    def generate(self):
        puml = execute(
            [
                'java',
                '-jar',
                self.proc.plantuml_jar_path,
                '-pipe',
                '-tpng'
            ],
            stdin=PIPE,
            stdout=self.file)
        puml.communicate(input=self.text)
        if puml.returncode != 0:
            print "Error Processing Diagram:"
            print self.text
            return
        else:
            return self.file


class PlantUMLProcessor(BaseProcessor):
    DIAGRAM_CLASS = PlantUMLDiagram
    PLANTUML_VERSION = 7232
    PLANTUML_VERSION_STRING = 'PlantUML version %s' % PLANTUML_VERSION

    def load(self):
        self.find_plantuml_jar()
        self.check_plantuml_version()

    def find_plantuml_jar(self):
        self.plantuml_jar_file = 'plantuml-%s.jar' % (self.PLANTUML_VERSION,)
        self.plantuml_jar_path = None

        self.plantuml_jar_path = abspath(
            join(
                dirname(__file__),
                self.plantuml_jar_file
            )
        )
        if not exists(self.plantuml_jar_path):
            raise Exception("can't find " + self.plantuml_jar_file)
        print "Detected %r" % (self.plantuml_jar_path,)

    def check_plantuml_version(self):
        puml = execute(
            [
                'java',
                '-jar',
                self.plantuml_jar_path,
                '-version'
            ],
            stdout=PIPE,
            stderr=STDOUT
        )
        version_output = ''
        first = True

        (stdout, stderr) = puml.communicate()
        version_output = stdout

        print "Version Detection:"
        print version_output

        if not puml.returncode == 0:
            raise Exception("PlantUML returned an error code")
        if self.PLANTUML_VERSION_STRING not in version_output:
            raise Exception("error verifying PlantUML version")

    def extract_blocks(self, view):
        pairs = (
            (
                start, view.find('@end', start.begin()))
                for start in view.find_all('@start')
            )
        return (view.full_line(start.cover(end)) for start, end in pairs)
