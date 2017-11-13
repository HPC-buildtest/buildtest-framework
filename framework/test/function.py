############################################################################
#
#  Copyright 2017
#
#   https://github.com/HPC-buildtest/buildtest-framework
#
#  This file is part of buildtest.
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

:author: Shahzeb Siddiqui (Pfizer)
"""

def add_arg_to_runcmd(runcmd,arglist):
        # add each argument to runcmd
        for arg in arglist:
        # skip argument if value is not specified, by default set to None
                if arg == None:
                        continue
                # in case argument is not a string, convert it anyways
                runcmd+= " " + str(arg)
        return runcmd

