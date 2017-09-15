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
from framework.parser.parser import *
from framework.testgen import *
from framework.tools.generic import *
import logging

def recursive_gen_test(configdir,codedir,verbose ):
        """ if config directory exists then process .yaml files to build source test """
	logger = logging.getLogger(logID)

	logger.debug("Processing all YAML files in %s", configdir)
	
        if os.path.isdir(configdir):
		count = 0
                for root,subdirs,files in os.walk(configdir):
    
                        #filepath=configdir+filename
                        for file in files:
                                filepath=os.path.join(root,file)
                                subdir=os.path.basename(root)
                                # if there is no subdirectory in configdir that means subdir would be set to "config" so it can
                                # be set to empty string in order to concat codedir and subdir. This way both subdirectory and 
                                # and no subdirectory structure for yaml will work
                                if subdir == "config":
                                        subdir = ""
                                code_destdir=os.path.join(codedir,subdir)
				logger.debug("Parsing YAML file: %s", filepath)
                                configmap=parse_config(filepath,code_destdir)    
                                # error processing config file, then parse_config will return an empty dictionary
                                if len(configmap) == 0:
                                        continue
				count = count + 1
                                generate_source_test(configmap,code_destdir,verbose,subdir)
		print "Generating " + str(count) + " Source Tests "

