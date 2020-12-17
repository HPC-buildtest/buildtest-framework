import os
import shutil
from buildtest.buildsystem.base import BuilderBase
from buildtest.menu.compilers import BuildtestCompilers
from buildtest.config import load_settings
from buildtest.exceptions import BuildTestError
from buildtest.utils.file import resolve_path
from buildtest.utils.tools import deep_get, Hasher


class CompilerBuilder(BuilderBase):
    type = "compiler"

    # Fortran Extensions Links:
    # https://software.intel.com/content/www/us/en/develop/documentation/fortran-compiler-developer-guide-and-reference/top/compiler-setup/using-the-command-line/understanding-file-extensions.html
    # Fortran Extensions: http://fortranwiki.org/fortran/show/File+extensions
    lang_ext_table = {
        ".c": "C",
        ".cc": "C++",
        ".cxx": "C++",
        ".cpp": "C++",
        ".c++": "C++",
        ".f90": "Fortran",
        ".F90": "Fortran",
        ".f95": "Fortran",
        ".f03": "Fortran",
        ".f": "Fortran",
        ".F": "Fortran",
        ".FOR": "Fortran",
        ".for": "Fortran",
        ".FTN": "Fortran",
        ".ftn": "Fortran",
    }

    default_compiler_settings = {"gcc": {}, "intel": {}, "pgi": {}, "cray": {}}

    cc = None
    cxx = None
    fc = None
    ldflags = None
    cflags = None
    cxxflags = None
    fflags = None
    cppflags = None
    executable = None

    def __init__(self, name, recipe, buildspec, compiler=None, testdir=None):
        super().__init__(name, recipe, buildspec, testdir)
        self.compiler = compiler
        self.bp_compiler = Hasher(self.recipe["compilers"])

        self.settings = load_settings()

        self.sourcefile = self.recipe["source"]

    def setup(self):
        """The setup method is responsible for process compiler section, getting modules
           pre_build, post_build, pre_run, post_run section and generate compilation
           and run command. This method invokes other methods and set values in class
           variables. This method is called by self.generate_script method.
        """

        self._resolve_source()
        self.lang = self._detect_lang(self.sourcefile)
        # set executable name and assign to self.executable
        self.executable = self._set_executable_name()

        self._process_compiler_config()
        self.modules = []

        # compiler set in compilers 'config' section, we try to get module lines using self._get_modules
        if self.bp_compiler.get(f"config.{self.compiler}"):
            self.modules = self._get_modules(
                self.bp_compiler.get(f"config.{self.compiler}module")
            )

        if not self.modules:
            self.modules = self._get_modules(self.bc_compiler.get("module"))

        self.pre_build = self.recipe.get("pre_build")
        self.post_build = self.recipe.get("post_build")
        self.pre_run = self.recipe.get("pre_run")
        self.post_run = self.recipe.get("post_run")

        self.compile_cmd = self._compile_cmd()

        self.run_cmd = self._run_cmd()

    def generate_script(self):
        """This method will build the test content from a Buildspec that uses compiler schema.
        We resolve the source file path which can be an absolute value or relative path with respect to Buildspec. The file extension of sourcefile is used
        to detect the Programming Language which is used to lookup the compiler wrapper based on Language + Compiler.
        During compiler detection, we set class variables ``self.cc``, ``self.cxx``. ``self.fc``, ``self.cflags``,
        ``self.cxxflags``, ``self.fflags``, ``self.cppflags``. ``self.ldflags``. Finally we generate the compile
        command and add each instruction to ``lines`` which contains content of test. Upon completion, we return
        a list that contains content of the test.
        """

        self.setup()

        # every test starts with shebang line
        # lines = [self.shebang]
        lines = []

        # get environment variables
        lines += self.get_environment()
        # get variables
        lines += self.get_variables()

        # if 'module' defined in Buildspec add modules to test
        if self.modules:
            lines += self.modules

        if self.pre_build:
            lines.append(self.pre_build)

        lines.append(self.compile_cmd)

        if self.post_build:
            lines.append(self.post_build)

        if self.pre_run:
            lines.append(self.pre_run)

        # add run command
        lines += self.run_cmd

        if self.post_run:
            lines.append(self.post_run)

        return lines

    def _resolve_source(self):
        """ This method resolves full path to source file, it checks for absolute
            path first before checking relative path that is relative to
            Buildspec recipe.
        """

        # attempt to resolve path based on 'source' field. One can specify an absolute path if specified we honor it
        self.resolvepath_sourcefile = resolve_path(self.sourcefile)
        # One can specify a relative path to where buildspec is located when using 'source' field so we try again
        if not self.resolvepath_sourcefile:
            self.resolvepath_sourcefile = resolve_path(
                os.path.join(os.path.dirname(self.buildspec), self.sourcefile)
            )

        # raise error if we can't find source file to compile
        if not self.resolvepath_sourcefile:
            raise BuildTestError(
                f"Failed to resolve path specified by key 'source': {self.sourcefile}"
            )

    def _detect_lang(self, sourcefile):
        """This method will return the Programming Language based by looking up
           file extension of source file.
        """

        ext = os.path.splitext(sourcefile)[1]

        # if ext not in self.lang_ext_table then raise an error. This table consist of all file extensions that map to a Programming Language
        if ext not in self.lang_ext_table:
            raise BuildTestError(
                f"Unable to detect Program Language based on extension: {ext} in file {sourcefile}"
            )
        # Set Programming Language based on ext. Programming Language could be (C, C++, Fortran)
        lang = self.lang_ext_table[ext]
        return lang

    def _get_modules(self, modules):
        """Return a list of modules as a list"""

        if not modules:
            return

        module_cmd = []

        assert isinstance(modules, dict)

        # if purge is True and defined add module purge
        if modules.get("purge"):
            module_cmd += ["module purge"]
        #
        if modules.get("load"):
            for name in modules.get("load"):
                module_cmd += [f"module load {name}"]

        if modules.get("swap"):
            module_cmd += [f"module swap {' '.join(modules.get('swap'))}"]

        if modules.get("restore"):
            module_cmd += [f"module restore {modules.get('restore')}"]
        return module_cmd

    def _compile_cmd(self):
        """This method generates the compilation line and returns the output as a list. The compilation line depends
        on the the language detected that is stored in variable ``self.lang``.
        """

        cmd = []
        # Generate C compilation line
        if self.lang == "C":
            cmd = [
                self.cc,
                self.cppflags,
                self.cflags,
                f"-o {self.executable}",
                self.resolvepath_sourcefile,
                self.ldflags,
            ]

        # Generate C++ compilation line
        elif self.lang == "C++":
            cmd = [
                self.cxx,
                self.cppflags,
                self.cxxflags,
                f"-o {self.executable}",
                self.resolvepath_sourcefile,
                self.ldflags,
            ]

        # Generate Fortran compilation line
        elif self.lang == "Fortran":
            cmd = [
                self.fc,
                self.cppflags,
                self.fflags,
                f"-o {self.executable}",
                self.resolvepath_sourcefile,
                self.ldflags,
            ]

        # remove any None from list
        cmd = list(filter(None, cmd))
        cmd = " ".join(cmd)

        return cmd

    def _run_cmd(self):
        """This method builds the run command which refers to how to run the
           generated binary after compilation.
        """

        self.run_dict = self.recipe.get("run")

        if not self.run_dict:
            return [f"./{self.executable}"]

        run = []

        # add launcher in front of execution if defined
        if self.run_dict.get("launcher"):
            run += [self.run_dict.get("launcher")]

        run += [f"./{self.executable}"]

        # add args after executable if defined
        run += [self.run_dict.get("args")]

        run = [" ".join(run)]

        return run

    def _set_executable_name(self, name=None):
        """This method set the executable name. One may specify a custom name to executable via ``name``
        argument. Otherwise the executable is using the filename of ``self.sourcefile`` and adding ``.exe``
        extension at end.
        """

        if name:
            return name

        return "%s.exe" % os.path.basename(self.sourcefile)

    def _process_compiler_config(self):

        # get default compiler definition
        if self.bp_compiler["default"]:
            for compiler in self.default_compiler_settings.keys():
                # if default section not defined for compiler we skip to next one
                if not deep_get(self.bp_compiler, "default", compiler):
                    continue

                for k, v in self.recipe["compilers"]["default"][compiler].items():
                    self.default_compiler_settings[compiler][k] = v

        bc = BuildtestCompilers()

        group = bc.compiler_name_to_group[self.compiler]

        # compiler from buildtest settings
        self.bc_compiler = self.settings["compilers"]["compiler"][group][self.compiler]

        # set compiler values based on 'default' property in buildspec. This can override
        # compiler setting defined in configuration file. If default is not set we load from buildtest settings for appropriate compiler.

        if self.default_compiler_settings.get(group):

            self.cc = (
                self.default_compiler_settings[group].get("cc")
                or self.bc_compiler["cc"]
            )
            self.fc = (
                self.default_compiler_settings[group].get("fc")
                or self.bc_compiler["fc"]
            )
            self.cxx = (
                self.default_compiler_settings[group].get("cxx")
                or self.bc_compiler["cxx"]
            )
            self.cflags = self.default_compiler_settings[group].get("cflags")
            self.cxxflags = self.default_compiler_settings[group].get("cxxflags")
            self.fflags = self.default_compiler_settings[group].get("fflags")
            self.ldflags = self.default_compiler_settings[group].get("ldflags")
            self.cppflags = self.default_compiler_settings[group].get("cppflags")

        # if compiler instance defined in config section read from buildspec
        if deep_get(self.bp_compiler, "config", self.compiler):
            self.cc = self.bp_compiler["config"][self.compiler].get("cc") or self.cc
            self.fc = self.bp_compiler["config"][self.compiler].get("fc") or self.fc
            self.cxx = self.bp_compiler["config"][self.compiler].get("cxx") or self.cxx
            self.cflags = (
                self.bp_compiler["config"][self.compiler].get("cflags") or self.cflags
            )
            self.cxxflags = (
                self.bp_compiler["config"][self.compiler].get("cxxflags")
                or self.cxxflags
            )
            self.fflags = (
                self.bp_compiler["config"][self.compiler].get("fflags") or self.fflags
            )
            self.cppflags = (
                self.bp_compiler["config"][self.compiler].get("cppflags")
                or self.cppflags
            )

    def set_cc(self, cc):
        self.cc = cc

    def set_cxx(self, cxx):
        self.cxx = cxx

    def set_fc(self, fc):
        self.fc = fc

    def set_cflags(self, cflags):
        self.cflags = cflags

    def set_fflags(self, fflags):
        self.fflags = fflags

    def set_cxxflags(self, cxxflags):
        self.cxxflags = cxxflags

    def set_cppflags(self, cppflags):
        self.cppflags = cppflags

    def set_ldflags(self, ldflags):
        self.ldflags = ldflags

    def get_cc(self):
        return self.cc

    def get_cxx(self):
        return self.cxx

    def get_fc(self):
        return self.fc

    def get_cflags(self):
        return self.cflags

    def get_cxxflags(self):
        return self.cxxflags

    def get_fflags(self):
        return self.fflags

    def get_cppfilags(self):
        return self.cppflags

    def get_ldflags(self):
        return self.ldflags

    def get_path(self):
        """ This method returns the full path for C, C++, Fortran compilers"""

        path = {
            self.cc: shutil.which(self.cc),
            self.cxx: shutil.which(self.cxx),
            self.fc: shutil.which(self.fc),
        }
        return path