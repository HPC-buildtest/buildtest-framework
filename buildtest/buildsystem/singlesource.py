"""
The file implements the singlesource build system responsible
"""

import logging
import os
import random
import yaml


from buildtest.config import config_opts
from buildtest.defaults import logID
from buildtest.utils.exceptions import BuildTestError


def get_yaml_schema():
    mpi_schema = {
        "type": dict,
        "required": False,
        "description": "MPI block for specifying mpi configuration.",
        "flavor": {
            "type": str,
            "required": False,
            "values": ["openmpi", "mpich"],
            "description": "Specify MPI Flavor. This is used to detect MPI wrapper.",
        },
        "launcher": {
            "type": str,
            "required": False,
            "values": ["mpirun", "mpiexec", "mpiexec.hydra"],
            "description": "Specify the MPI Launcher to run MPI jobs",
        },
        "launcher_opts": {
            "type": str,
            "required": False,
            "description": "Pass options to MPI Launcher",
        },
    }
    schema = {
        "testtype": {
            "type": str,
            "required": True,
            "values": "singlesource",
            "description": "Buildtest Class for Single Source Compilation",
        },
        "description": {
            "type": str,
            "required": True,
            "description": "Description Text for test configuration limited to 80 characters",
        },
        "maintainer": {
            "type": list,
            "required": True,
            "description": "List of Maintainers for the test",
        },
        "moduleload": {
            "type": dict,
            "required": False,
            "description": "Specify type of method to load modules into test.",
            "lmod_collection": {
                "type": str,
                "required": False,
                "description": "Specify a Lmod Collection name to load in test",
            },
        },
        "mpi": {
            "type": bool,
            "required": False,
            "values": [False, True],
            "description": "Instruct buildtest if this test is a MPI test",
        },
        "program": {
            "type": dict,
            "required": True,
            "description": "Start of Program. This section where you specify test parameters.",
            "source": {
                "type": str,
                "required": True,
                "description": "Source File to compile. This file must be in 'src' directory",
            },
            "compiler": {
                "type": str,
                "required": True,
                "values": ["gnu", "intel", "pgi", "cuda", "clang"],
                "description": "Specify Compiler Name to detect compiler wrapper.",
            },
            "env": {
                "type": dict,
                "required": False,
                "description": "Specify List of Environment Varaibles in Test",
            },
            "cflags": {
                "type": str,
                "required": False,
                "description": "Specify compiler flags to C compiler (i.e $CC)",
            },
            "cxxflags": {
                "type": str,
                "required": False,
                "description": "Specify compiler flags to C++ compiler (i.e $CXX)",
            },
            "fflags": {
                "type": str,
                "required": False,
                "description": "Specify compiler flags to Fortran compiler (i.e $FC)",
            },
            "ldflags": {
                "type": str,
                "required": False,
                "description": "Specify linker flags",
            },
            "pre_build": {
                "type": str,
                "required": False,
                "description": "Shell commands to run before building.",
            },
            "post_build": {
                "type": str,
                "required": False,
                "description": "Shell commands to run after building.",
            },
            "pre_run": {
                "type": str,
                "required": False,
                "description": "Shell commands to run before running executable.",
            },
            "post_run": {
                "type": str,
                "required": False,
                "description": "Shell commands to run after running executable.",
            },
            "pre_exec": {
                "type": str,
                "required": False,
                "description": "Command in front of executable.",
            },
            "exec_opts": {
                "type": str,
                "required": False,
                "description": "Passing options to executable.",
            },
            "post_exec": {
                "type": str,
                "required": False,
                "description": "Commands after executable.",
            },
            "mpi": mpi_schema,
        },
    }
    return schema


class BuildTestBuilder:
    """Class responsible for parsing the test configuration."""

    def __init__(self, file, compiler=None, mpi=False):
        """Class constructor for BuildTestBuilder"""

        self.ext = os.path.splitext(file)[1]
        self.compiler = compiler or None
        self.mpi = mpi
        self.cc = None
        self.cxx = None
        self.ftn = None
        self.nvcc = None
        self.cflags = None
        self.cxxflags = None
        self.cppflags = None
        self.fflags = None
        self.ldflags = None
        self.language = None

        self._detect_language()
        self._detect_compiler()
        if self.mpi:
            self._detect_mpi()

    def get_cc(self):
        """Return cc variable"""

        return self.cc

    def get_cxx(self):
        """Return cxx variable"""
        return self.cxx

    def get_ftn(self):
        """Return ftn variable"""
        return self.ftn

    def get_nvcc(self):
        """Return cc variable"""
        return self.nvcc

    def get_cflags(self):
        """Return cflags variable"""
        return self.cflags

    def get_fflags(self):
        """Return fflags variable"""
        return self.fflags

    def get_ldflags(self):
        """Return fflags variable"""
        return self.ldflags

    def get_language(self):
        """Return language variable."""
        return self.language

    def _detect_language(self):
        """ Return Programming Language  based on extension

        :param ext: File extension of source file
        :type ext: str, required
        :return: return programming language
        :rtype: str
        """

        # checking C extensions
        if self.ext in [".c"]:
            self.language = "c"

        # checking C++ extensions
        elif self.ext in [".cc", ".cxx", ".cpp", ".c++", ".C"]:
            self.language = "c++"

        # checking Fortran extensions
        elif self.ext in [
            ".f90",
            ".f95",
            ".f03",
            ".f",
            ".F",
            ".F90",
            ".FPP",
            ".FOR",
            ".FTN",
            ".for",
            ".ftn",
        ]:
            self.language = "fortran"

        # checking cuda extensions
        elif self.ext in [".cu"]:
            self.language = "cuda"

        # if all checks failed then raise error
        else:
            raise BuildTestError(
                f"Unable to detect Program Language based on extension: {self.ext}"
            )

    def _detect_compiler(self):
        """Detect compiler based on language

        :param language: Language type
        :type language: str, required
        :param compiler: Compiler Type
        :type compiler: str, required
        :return: return compiler wrapper
        :rtype: str
        """
        """
        compiler_lookup = {
            "gnu": ["gcc","gfortran","g++"],
            "intel": ["icc","ifort","icpc"],
            "pgi": ["pgcc", "pgfortran", "pgc++"],
            "clang": ["clang","clang++"],
            "cuda": ["nvcc"]
        }
        """

        if self.compiler == "gnu":
            if self.language == "c":
                self.cc = "gcc"

            elif self.language == "c++":
                self.cxx = "g++"

            elif self.language == "fortran":
                self.ftn = "gfortran"

        elif self.compiler == "intel":
            if self.language == "c":
                self.cc = "icc"

            elif self.language == "c++":
                self.cxx = "icpc"

            elif self.language == "fortran":
                self.ftn = "ifort"

        elif self.compiler == "pgi":
            if self.language == "c":
                self.cc = "pgcc"

            elif self.language == "c++":
                self.cxx = "pgc++"

            elif self.language == "fortran":
                self.ftn = "pgfortran"

        elif self.compiler == "clang":
            if self.language == "c":
                self.cc = "clang"
            elif self.language == "c++":
                self.cxx = "clang++"

        elif self.compiler == "cuda":
            self.nvcc = "nvcc"

    def _detect_mpi(self):
        """Detect MPI wrapper based on Language and compiler.

        :param language: Language type
        :type language: str, required
        :param compiler: Compiler Type
        :type compiler: str

        :return: return compiler wrapper
        :rtype: str
        """
        if self.language == "c" and self.compiler == "gnu":
            self.cc = "mpicc"

        if self.language == "c++" and self.compiler == "gnu":
            self.cxx = "mpicxx"
        if self.language == "fortran" and self.compiler == "gnu":
            self.ftn = "mpifort"

        if self.language == "c" and self.compiler == "intel":
            self.cc = "mpiicc"
        if self.language == "c++" and self.compiler == "intel":
            self.cxx = "mpiicpc"
        if self.language == "fortran" and self.compiler == "intel":
            self.ftn = "mpiifort"


class SingleSource(BuildTestBuilder):
    def __init__(self, config_file, lmod_collection=None, buildtest_collection=None):
        """Class constructor for SingleSource"""
        self.lmod_collection = lmod_collection
        self.buildtest_collection = buildtest_collection
        self.config_file = config_file

        self.schema = get_yaml_schema()
        if not config_file:
            return

        logger = logging.getLogger(logID)

        with open(config_file, "r") as fd:
            self.test_yaml = yaml.safe_load(fd)

        print("{:<40} {}".format("[LOAD CONFIG]", "PASSED"))

        self.check_top_keys()

        # self.mpi used to enable/disable mpi check
        self.mpi = False
        self.parent_dir = os.path.dirname(config_file)
        self.srcdir = os.path.join(self.parent_dir, "src")

        # content to store the test script
        self.testscript_content = {
            "testpath": "",
            "shell": ["#!/bin/bash"],
            "module": [],
            "metavars": [],
            "envs": [],
            "build": [],
            "run": [],
        }

        self.envs = []
        # moduleload_check is enabled if "moduleload" key is defined, then buildtest will attempt to resolve module based
        # on configuration file
        self.moduleload_check = False
        self.check_program_keys()
        print("{:<40} {}".format("[SCHEMA CHECK]", "PASSED"))

        if "mpi" in self.test_yaml.keys():
            self.mpi = self.test_yaml["mpi"]

        if "moduleload" in self.test_yaml.keys():
            self.moduleload_check = True
            if "lmod_collection" in self.test_yaml["moduleload"].keys():
                self.lmod_collection = self.test_yaml["moduleload"]["lmod_collection"]

        # self.srcfile = os.path.join(self.srcdir, self.test_yaml["program"]["source"])
        self.srcfile = self.test_yaml["program"]["source"]

        # Generate a common hex to identify and link exec and script file
        randhex = hex(random.getrandbits(32))

        self.execname = "%s.%s.exec" % (os.path.basename(config_file), randhex)

        # invoke setup method from base class to detect language, compiler, and mpi wrapper
        self.testscript_content["testpath"] = "%s.%s.sh" % (
            os.path.join(
                config_opts["build"]["testdir"], os.path.basename(config_file)
            ),
            randhex,
        )

        logger.debug(f"Source Directory: {self.srcdir}")
        logger.debug(f"Source File: {self.srcfile}")

        super().__init__(self.srcfile, self.test_yaml["program"]["compiler"], self.mpi)
        print("{:<40} {}".format("[PROGRAM LANGUAGE]", self.language))
        print("{:<40} {}".format("[COMPILER NAME]", self.compiler))

        self.buildcmd = self.build_command()

    def __str__(self):
        return "SingleSource: %s" % os.path.basename(self.config_file)

    def __repr__(self):
        return self.__str__()

    def get_schema(self):
        """Return the yaml schema for singlesource class."""
        return self.schema

    def check_top_keys(self):
        """Check Top Level Keys in self.schema dictionary"""

        for k in self.schema.keys():
            # print (self.schema[k]['required'],k,test_keys.keys(),k not in test_keys.keys())
            # print (self.schema[k]['required'], k not in test_keys.keys())

            # if required key not found in test configuration then report error.
            if self.schema[k]["required"] and (k not in self.test_yaml.keys()):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # check instance type of key in test configuration and match with one defined in self.schema.
            if k in self.test_yaml.keys() and not isinstance(
                self.test_yaml[k], self.schema[k]["type"]
            ):
                raise BuildTestError(
                    f"Expecting of type: {self.schema[k]['type']} and received of type: {type(self.test_yaml[k])}"
                )

            # value of key must be testtype: singlesource
            if (
                k == "testtype"
                and self.test_yaml["testtype"] != self.schema["testtype"]["values"]
            ):
                raise BuildTestError(
                    f"Key must be testtype: singlesource. Received {k}:{self.test_yaml['testtype']}"
                )

            # description text can't be more than 80 chars
            if k == "description" and len(self.test_yaml["description"]) > 80:
                raise BuildTestError(
                    "Description can't be more than 80 characters."
                    f"Length: {len(self.test_yaml['description'])} "
                    f"{k}:{self.test_yaml['description']}"
                )

            # check scheduler value types
            if (
                k == "scheduler"
                and self.test_yaml["scheduler"]
                not in self.schema["scheduler"]["values"]
            ):
                raise BuildTestError(
                    f"{self.test_yaml['scheduler']} is not valid value. Must be one of the following: {self.schema['scheduler']['values']}"
                )

            # first check if "mpi" key is in test configuration because it is not a required key
            if k == "mpi" and "mpi" in self.test_yaml:
                # if found, then check value type. By default, if it is not found, mpi will be disabled
                if self.test_yaml["mpi"] not in self.schema["mpi"]["values"]:
                    raise BuildTestError(
                        f"{self.test_yaml['mpi']} is not valid value. Must be one of the following: {self.schema['mpi']['values']}"
                    )

    def check_program_keys(self):
        """Check keys in dictionary program:"""
        # enable mpi key in program dictionary if self.mpi == yes
        if self.mpi:
            self.schema["program"]["mpi"]["required"] = True
            self.schema["program"]["mpi"]["flavor"]["required"] = True
            self.schema["program"]["mpi"]["launcher"]["required"] = True

        # type check for top level program key
        if not isinstance(self.test_yaml["program"], self.schema["program"]["type"]):
            raise BuildTestError(
                f"Expecting of type: {self.schema['program']['type']} for program key. Received of type: {self.test_yaml['program']}"
            )

        for k in self.schema["program"].keys():
            # skip keys of they are "type" or "required" or "description" these are metadata for program key
            if k in ["type", "required", "description"]:
                continue
            # if required key not found in test configuration then report error.
            if self.schema["program"][k]["required"] and (
                k not in self.test_yaml["program"].keys()
            ):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # skip to next key if not found in test configuration.
            if k not in self.test_yaml["program"].keys():
                continue
            # check instance type of key in test configuration and match with one defined in self.schema.
            if not isinstance(
                self.test_yaml["program"][k], self.schema["program"][k]["type"]
            ):
                raise BuildTestError(
                    f"Expecting of type: {self.schema['program'][k]['type']} and received of type: {type(self.test_yaml['program'][k])}"
                )

            if k == "compiler":
                if (
                    self.test_yaml["program"][k]
                    not in self.schema["program"][k]["values"]
                ):
                    raise BuildTestError(
                        f"Expecting value for {k}: {self.schema['program'][k]['values']} and received value: {self.test_yaml['program'][k]}"
                    )

            if k == "mpi":
                self.check_mpi_keys()

    def check_mpi_keys(self):
        """Check program:mpi keys."""

        for k in self.schema["program"]["mpi"].keys():

            if k in ["type", "required", "description"]:
                continue
            # if required key not found in test configuration then report error.
            if (
                self.schema["program"]["mpi"][k]["required"]
                and k not in self.test_yaml["program"]["mpi"].keys()
            ):
                raise BuildTestError(f"Key: {k} is required in test configuration!")

            # check instance type of key in test configuration and match with one defined in self.schema.
            if not isinstance(
                self.test_yaml["program"]["mpi"][k],
                self.schema["program"]["mpi"][k]["type"],
            ):
                raise BuildTestError(
                    f"Expecting of type: {self.schema['program']['mpi'][k]['type']} and received of type: {type(self.test_yaml['program']['mpi'][k])}"
                )

            # checking value of mpi flavor confirm with valid value in self.schema
            if (
                k == "flavor"
                and self.test_yaml["program"]["mpi"]["flavor"]
                not in self.schema["program"]["mpi"]["flavor"]["values"]
            ):
                raise BuildTestError(
                    f"{self.test_yaml['program']['mpi']['flavor']} is not valid value. Must be one of the following: {self.schema['program']['mpi']['flavor']['values']}"
                )

            # checking value of mpi flavor confirm with valid value in self.schema
            if (
                k == "launcher"
                and self.test_yaml["program"]["mpi"]["launcher"]
                not in self.schema["program"]["mpi"]["launcher"]["values"]
            ):
                raise BuildTestError(
                    f"{self.test_yaml['program']['mpi']['launcher']} is not valid value. Must be one of the following: {self.schema['program']['mpi']['launcher']['values']}"
                )

    def build_command(self):
        """Generate the compilation command based on language and compiler. """

        if "env" in self.test_yaml["program"]:
            for k, v in self.test_yaml["program"]["env"].items():
                self.envs.append(["export", f"{k}={v}"])

        buildcmd = []

        if self.language == "c":
            # check if cflags is defined
            if "cflags" in self.test_yaml["program"]:
                self.cflags = self.test_yaml["program"]["cflags"]
                buildcmd = ["$CC", "$CFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$CC", "-o", "$EXECUTABLE", "$SRCFILE"]

        elif self.language == "c++":
            # check if cflags is defined
            if "cxxflags" in self.test_yaml["program"]:
                self.cxxflags = self.test_yaml["program"]["cxxflags"]
                buildcmd = ["$CXX", "$CXXFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$CXX", "-o", "$EXECUTABLE", "$SRCFILE"]

        elif self.language == "fortran":
            # check if cflags is defined
            if "fflags" in self.test_yaml["program"]:
                self.fflags = self.test_yaml["program"]["fflags"]
                buildcmd = ["$FC", "$FFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$FC", "-o", "$EXECUTABLE", "$SRCFILE"]

        elif self.language == "cuda":
            # check if cflags is defined
            if "cflags" in self.test_yaml["program"]:
                self.cflags = self.test_yaml["program"]["cflags"]
                buildcmd = ["$CC", "$CFLAGS", "-o", "$EXECUTABLE", "$SRCFILE"]
            else:
                buildcmd = ["$CC", "-o", "$EXECUTABLE", "$SRCFILE"]

        if "ldflags" in self.test_yaml["program"]:
            self.ldflags = self.test_yaml["program"]["ldflags"]
            buildcmd.append("$LDFLAGS")

        return buildcmd

    def build_test_content(self):
        """This method brings all the components together to form the test structure."""

        logger = logging.getLogger(logID)

        self.testscript_content["metavars"].append(
            f"TESTDIR={config_opts['build']['testdir']}"
        )
        self.testscript_content["metavars"].append(f"SRCDIR={self.srcdir}")
        self.testscript_content["metavars"].append(f"SRCFILE=$SRCDIR/{self.srcfile}")

        if self.cc:
            self.testscript_content["metavars"].append(f"CC={self.cc}")

        if self.nvcc:
            self.testscript_content["metavars"].append(f"CC={self.nvcc}")

        if self.ftn:
            self.testscript_content["metavars"].append(f"FC={self.ftn}")

        if self.cxx:
            self.testscript_content["metavars"].append(f"CXX={self.cxx}")

        if self.cflags:
            self.testscript_content["metavars"].append(f'CFLAGS="{self.cflags}"')

        if self.cxxflags:
            self.testscript_content["metavars"].append(f'CXXFLAGS="{self.cxxflags}"')

        if self.fflags:
            self.testscript_content["metavars"].append(f'FFLAGS="{self.fflags}"')
        if self.ldflags:
            self.testscript_content["metavars"].append(f'LDFLAGS="{self.ldflags}"')

        if self.execname:
            self.testscript_content["metavars"].append(f"EXECUTABLE={self.execname}")

        # adding environment variables
        for k in self.envs:
            self.testscript_content["envs"].append(" ".join(k))

        self.testscript_content["build"].append("cd $TESTDIR")

        if "pre_build" in self.test_yaml["program"].keys():
            self.testscript_content["build"].append(
                self.test_yaml["program"]["pre_build"]
            )

        self.testscript_content["build"].append(" ".join(self.buildcmd))

        if "post_build" in self.test_yaml["program"].keys():
            self.testscript_content["build"].append(
                self.test_yaml["program"]["post_build"]
            )

        if "pre_run" in self.test_yaml["program"].keys():
            self.testscript_content["run"].append(self.test_yaml["program"]["pre_run"])

        exec_cmd = []
        if "pre_exec" in self.test_yaml["program"].keys():
            exec_cmd.append(self.test_yaml["program"]["pre_exec"])

        if self.mpi:
            exec_cmd.append(self.test_yaml["program"]["mpi"]["launcher"])
            exec_cmd.append(self.test_yaml["program"]["mpi"]["launcher_opts"])

        exec_cmd.append("$EXECUTABLE")

        if "exec_opts" in self.test_yaml["program"].keys():
            exec_cmd.append(self.test_yaml["program"]["exec_opts"])

        if "post_exec" in self.test_yaml["program"].keys():
            exec_cmd.append(self.test_yaml["program"]["post_exec"])

        self.testscript_content["run"].append(" ".join(exec_cmd))

        if "post_run" in self.test_yaml["program"].keys():
            self.testscript_content["run"].append(self.test_yaml["program"]["post_run"])

        self.testscript_content["run"].append(f"rm ./$EXECUTABLE")
        for k, v in self.testscript_content.items():
            logger.debug(f"{k}:{v}")

        return self.testscript_content
