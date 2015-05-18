from __future__ import absolute_import
from .base import BaseDiagram
from .base import BaseProcessor
from subprocess import Popen as execute, PIPE, STDOUT, call
from os.path import abspath, dirname, exists, join
from tempfile import NamedTemporaryFile
from platform import system

IS_MSWINDOWS = (system() == 'Windows')
CREATE_NO_WINDOW = 0x08000000  # See MSDN, http://goo.gl/l4OKNe
EXTRA_CALL_ARGS = {'creationflags': CREATE_NO_WINDOW} if IS_MSWINDOWS else {}


class PlantUMLDiagram(BaseDiagram):
    def __init__(self, processor, sourceFile, text):
        super(PlantUMLDiagram, self).__init__(processor, sourceFile, text)
        self.file = NamedTemporaryFile(prefix=sourceFile, suffix='.png', delete=False)

    def generate(self):
        command = [
            'java',
            '-jar',
            self.proc.plantuml_jar_path,
            '-pipe',
            '-tpng',
            '-charset',
            'UTF-8'
        ]

        charset = self.proc.CHARSET
        if charset:
            print('using charset: ' + charset)
            command.append("-charset")
            command.append(charset)

        puml = execute(
            command,
            stdin=PIPE, stdout=self.file,
            **EXTRA_CALL_ARGS
        )
        puml.communicate(input=self.text.encode('UTF-8'))
        if puml.returncode != 0:
            print("Error Processing Diagram:")
            print(self.text)
            return
        else:
            return self.file


class PlantUMLProcessor(BaseProcessor):
    DIAGRAM_CLASS = PlantUMLDiagram
    PLANTUML_VERSION = 8024
    PLANTUML_VERSION_STRING = 'PlantUML version %s' % PLANTUML_VERSION

    def load(self):
        self.check_dependencies()
        self.find_plantuml_jar()

        if self.CHECK_ON_STARTUP:
            self.check_plantuml_version()
            self.check_plantuml_functionality()

    def check_dependencies(self):
        has_java = call(
            ["java", "-version"],
            **EXTRA_CALL_ARGS
        )

        if has_java is not 0:
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
            stderr=STDOUT,
            **EXTRA_CALL_ARGS
        )

        (stdout, stderr) = puml.communicate()
        dot_output = str(stdout)

        print("PlantUML Smoke Check:")
        print(dot_output)

        if ('OK' not in dot_output) or ('Error' in dot_output):
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
        print("Detected %r" % (self.plantuml_jar_path,))

    def check_plantuml_version(self):
        puml = execute(
            [
                'java',
                '-jar',
                self.plantuml_jar_path,
                '-version'
            ],
            stdout=PIPE,
            stderr=STDOUT,
            **EXTRA_CALL_ARGS
        )

        (stdout, stderr) = puml.communicate()
        version_output = stdout

        print("Version Detection:")
        print(version_output)

        if not puml.returncode == 0:
            raise Exception("PlantUML returned an error code")
        if self.PLANTUML_VERSION_STRING not in str(version_output):
            raise Exception("error verifying PlantUML version")

    def extract_blocks(self, view):
		# If any Region is selected - trying to convert it, otherwise converting all @start-@end blocks in view
        sel = view.sel()
        if sel[0].a == sel[0].b:
            pairs = (
                    (start, view.find('@end', start.begin()),)
                    for start in view.find_all('@start')
                )
            return (view.full_line(start.cover(end)) for start, end in pairs)
        else:
            return sel
