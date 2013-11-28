from __future__ import absolute_import
from .base import BaseDiagram
from .base import BaseProcessor
from subprocess import Popen as execute, PIPE, STDOUT, check_call
from os import rename
from os.path import abspath, dirname, exists, join, splitext
from tempfile import NamedTemporaryFile
from sys import platform

def custom_print(value):
    print("  *  [" + __name__ + "] " + value)

class PlantUMLDiagram(BaseDiagram):

    def generate(self):

        source_file = NamedTemporaryFile(suffix='.wsd', delete=False)
        custom_print("source_file.name = " + source_file.name)
        with open(source_file.name, "w") as text_file:
            text_file.write(self.text.encode('UTF-8'))

        self.command = 'java -jar' + ' \"' + self.proc.plantuml_jar_path + '\"' + ' -charset UTF-8' + ' \"' + source_file.name + '\"'
        custom_print("command = " + self.command)

        puml = execute(self.command)
        puml.communicate()

        if puml.returncode != 0:
            custom_print("Error Processing Diagram, ret.code = " + str(puml.returncode))
            # custom_print(self.text)
            return
        else:
            self.file = open(splitext(source_file.name)[0] + ".png")
            custom_print("output filename = " + self.file.name)
            return self.file

class PlantUMLProcessor(BaseProcessor):
    DIAGRAM_CLASS = PlantUMLDiagram
    PLANTUML_VERSION = 7986
    PLANTUML_VERSION_STRING = 'PlantUML version %s' % PLANTUML_VERSION

    def load(self):
        self.check_dependencies()
        self.find_plantuml_jar()
        # self.check_plantuml_version()
        # self.check_plantuml_functionality()

    def check_dependencies(self):
        custom_print("os platform: " + platform)
        if(platform not in ("win32",)):
            if not check_call("which java > /dev/null", shell=True) == 0:
                raise Exception("can't find Java")

    def check_plantuml_functionality(self):
        puml = execute(
            [
                'java',
                '-jar',
                self.plantuml_jar_path,
                '-testdot'
            ],
            stdout=PIPE,
            stderr=STDOUT
        )

        (stdout, stderr) = puml.communicate()
        dot_output = str(stdout)

        custom_print("PlantUML Smoke Check:")
        custom_print(dot_output)

        if (not 'OK' in dot_output) or ('Error' in dot_output):
            raise Exception('PlantUML does not appear functional')

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
        custom_print("Detected %r" % (self.plantuml_jar_path,))

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

        (stdout, stderr) = puml.communicate()
        version_output = stdout

        custom_print("Version Detection:")
        custom_print(version_output)

        if not puml.returncode == 0:
            raise Exception("PlantUML returned an error code")
        if self.PLANTUML_VERSION_STRING not in str(version_output):
            raise Exception("error verifying PlantUML version")

    def extract_blocks(self, view):
        pairs = (
            (
                start, view.find('@end', start.begin()))
                for start in view.find_all('@start')
            )
        return (view.full_line(start.cover(end)) for start, end in pairs)
