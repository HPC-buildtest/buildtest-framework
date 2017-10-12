############################################################################ 
# 
#  Copyright 2017 
# 
#   https://github.com/HPC-buildtest/buildtest-framework 
# 
#    This file is part of buildtest. 
# 
#    buildtest is free software: you can redistribute it and/or modify 
#    it under the terms of the GNU General Public License as published by 
#    the Free Software Foundation, either version 3 of the License, or 
#    (at your option) any later version. 
# 
#    buildtest is distributed in the hope that it will be useful, 
#    but WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
#    GNU General Public License for more details. 
# 
#    You should have received a copy of the GNU General Public License 
#    along with buildtest.  If not, see <http://www.gnu.org/licenses/>. 
############################################################################# 

"""
This file sets the buildtest specific environment variables used throughout all
the scripts

:author: Shahzeb Siddiqui (Pfizer)
"""

import os

# read the BUILDTEST env vars from the shell environment that is sourced by setup.sh
BUILDTEST_VERSION="1.2.0"
BUILDTEST_ROOT = os.environ['BUILDTEST_ROOT']
BUILDTEST_SOURCEDIR = os.environ['BUILDTEST_SOURCEDIR']
BUILDTEST_EASYCONFIGDIR = os.environ['BUILDTEST_EASYCONFIGDIR']
BUILDTEST_MODULE_EBROOT = os.environ['BUILDTEST_MODULE_EBROOT']
BUILDTEST_MODULE_NAMING_SCHEME = os.environ['BUILDTEST_MODULE_NAMING_SCHEME']
BUILDTEST_TESTDIR = os.environ['BUILDTEST_TESTDIR']


PYTHON_APPS = ["Python","Anaconda2", "Anaconda3"]
MPI_APPS = ["OpenMPI", "MPICH","MVAPICH2", "intel", "impi"]

global logID
logID = "buildtest"

global BUILDTEST_LOGCONTENT
BUILDTEST_LOGDIR = os.path.join(BUILDTEST_ROOT,"log")
BUILDTEST_LOGCONTENT = []

	
