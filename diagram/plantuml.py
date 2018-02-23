from __future__ import absolute_import
from .base import BaseDiagram
from .base import BaseProcessor
from subprocess import Popen as execute, PIPE, STDOUT, call
from os import getcwd, chdir
from os.path import abspath, dirname, exists, join, splitext
from tempfile import NamedTemporaryFile
from sublime import platform

import sys
if sys.version_info < (3,0):
    import os
    DEVNULL = open(os.devnull, 'wb')
else:
    from subprocess import DEVNULL

IS_MSWINDOWS = (platform() == 'windows')
CREATE_NO_WINDOW = 0x08000000  # See MSDN, http://goo.gl/l4OKNe
EXTRA_CALL_ARGS = {'creationflags': CREATE_NO_WINDOW, 'shell': True} if IS_MSWINDOWS else {}
OUTPUT_FORMAT_DICT = {
    'png':   ('-tpng',   '.png'),   # generate images using PNG format
    'svg':   ('-tsvg',   '.svg'),   # generate images using SVG format
    'txt':   ('-ttxt',   '.txt'),   # generate images with ASCII art
    'utxt':  ('-tutxt',  '.utxt'),  # generate images with ASCII art using Unicode characters
    'latex': ('-tlatex', '.tex')   # generate images using LaTeX/Tikz format
    # ------------------------------
    # These formats are also supported by plantUml, but they need some prerequisite to be installed...
    # PlantUml return_code = 1 on invocation.
    # 'pdf':   ('-tpdf',   '.pdf'),   # generate images using PDF format
    # 'vdx':   ('-tvdx',   '.vdx'),   # generate images using VDX format
    # 'eps':   ('-teps',   '.eps'),   # generate images using EPS format
}

class PlantUMLDiagram(BaseDiagram):
    def __init__(self, processor, sourceFile, text):
        super(PlantUMLDiagram, self).__init__(processor, sourceFile, text)

        output_format = self.proc.OUTPUT_FORMAT
        self.output_format_arg, self.output_file_extension = OUTPUT_FORMAT_DICT.get(output_format, (None, None))
        if not self.output_format_arg:
            raise Exception("Unsupported value '%s' for setting 'output_format'" % (output_format))

        self.workDir = None
        if sourceFile is None:
            self.file = NamedTemporaryFile(prefix='untitled', suffix=self.output_file_extension, delete=False)
        else:
            sourceDir = dirname(sourceFile)
            if exists(sourceDir):
                self.workDir = sourceDir
            if self.proc.NEW_FILE:
                self.file = NamedTemporaryFile(prefix=sourceFile, suffix=self.output_file_extension, delete=False)
            else:
                sourceFile = splitext(sourceFile)[0] + self.output_file_extension
                self.file = open(sourceFile, 'w')

    def generate(self):
        """
        Set the dir of sourceFile as working dir, otherwise plantuml could not include files correctly.
        """
        cwd = getcwd()
        if self.workDir:
            print ('chdir to:', self.workDir)
            chdir(self.workDir)

        try:
            return self._generate()
        finally:
            if self.workDir:
                chdir(cwd)

    def _generate(self):

        # http://en.plantuml.com/command-line
        command = [
            'java',
            '-DPLANTUML_LIMIT_SIZE=50000', # max output image height
            '-jar',
            self.proc.plantuml_jar_path,
            '-pipe',
            self.output_format_arg
        ]

        charset = self.proc.CHARSET
        if charset:
            print('using charset: ' + charset)
            command.append("-charset")
            command.append(charset)
        else:
            print('using default charset: UTF-8')
            command.append("-charset")
            command.append('UTF-8')

        print("Command: %s" % (command))

        puml = execute(
            command,
            stdin=PIPE,
            stdout=self.file,
            stderr=DEVNULL,
            **EXTRA_CALL_ARGS
        )
        puml.communicate(input=self.text.encode('UTF-8'))
        if puml.returncode != 0:
            print("Error Processing Diagram, returncode=%s:" % (puml.returncode))
            print(self.text)
            return
        else:
            return self.file

class PlantUMLProcessor(BaseProcessor):
    DIAGRAM_CLASS = PlantUMLDiagram
    PLANTUML_VERSION = '1.2018.1'
    PLANTUML_VERSION_STRING = 'PlantUML version 1.2018.01'

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
            raise Exception("Can't find Java")

    def check_plantuml_functionality(self):
        puml = execute(
            [
                'java',
                '-jar',
                self.plantuml_jar_path,
                '-testdot'
            ],
            stdin=DEVNULL,
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
        self.plantuml_jar_file = 'plantuml.%s.jar' % (self.PLANTUML_VERSION,)
        self.plantuml_jar_path = None

        self.plantuml_jar_path = abspath(
            join(
                dirname(__file__),
                self.plantuml_jar_file
            )
        )
        if not exists(self.plantuml_jar_path):
            raise Exception("Can't find " + self.plantuml_jar_file)
        print("Detected %r" % (self.plantuml_jar_path,))

    def check_plantuml_version(self):
        puml = execute(
            [
                'java',
                '-jar',
                self.plantuml_jar_path,
                '-version'
            ],
            stdin=DEVNULL,
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
            raise Exception("Error verifying PlantUML version")

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
