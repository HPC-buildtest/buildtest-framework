#!/usr/bin/env python
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
The entry point to buildtest

:author: Shahzeb Siddiqui (Pfizer)
"""

import sys
import os
import subprocess
import argparse
import logging
from datetime import datetime
import glob
sys.path.insert(0,os.path.abspath('.'))


from framework.env import BUILDTEST_ROOT, BUILDTEST_LOGDIR, BUILDTEST_MODULE_NAMING_SCHEME, BUILDTEST_SOURCEDIR, BUILDTEST_TESTDIR, BUILDTEST_MODULE_EBROOT, BUILDTEST_EASYCONFIGDIR, BUILDTEST_JOB_EXTENSION, logID
from framework.runtest import runtest_menu
from framework.test.binarytest import generate_binary_test
from framework.test.job import submit_job_to_scheduler
from framework.test.sourcetest import recursive_gen_test
from framework.test.testsets import run_testset
from framework.tools.check_setup import check_buildtest_setup
from framework.tools.find import find_all_yaml_configs, find_yaml_configs_by_arg
from framework.tools.find import find_all_tests, find_tests_by_arg
from framework.tools.easybuild import list_toolchain, check_software_version_in_easyconfig
from framework.tools.generate_yaml import create_system_yaml
from framework.tools.menu import buildtest_menu
from framework.tools.print_functions import print_software_version_relation
from framework.tools.scan import scantest
from framework.tools.software import get_unique_software, software_version_relation 
from framework.tools.utility import  print_set
from framework.tools.utility import get_appname, get_appversion, get_toolchain_name, get_toolchain_version
from framework.tools.version import buildtest_version

def main():
	""" entry point to buildtest """
	#module=""
	#version=""


	parser = buildtest_menu()
	bt_opts = parser.parse_options()

	if bt_opts.version:
		buildtest_version()
		sys.exit(0)

	if bt_opts.check_setup:
		check_buildtest_setup()
		sys.exit(1)

	if bt_opts.runtest:
		runtest_menu()
	
	if bt_opts.scantest:
		scantest()

	if bt_opts.list_toolchain is True:
                toolchain_set=list_toolchain()
                text = """ \n
                         List of Toolchains:
                         -------------------- \n"""
                print text
                print_set(toolchain_set)

                sys.exit(0)

        if bt_opts.list_unique_software:
                software_set=get_unique_software()
                text =  """ \n
                       List of Unique Software:
                       ---------------------------- \n """
                print text
                print_set(software_set)

                sys.exit(0)

        if bt_opts.software_version_relation:
                software_dict = software_version_relation()
		print_software_version_relation(software_dict)
                sys.exit(0)

	if bt_opts.job_template is not None:
		if not os.path.isfile(bt_opts.job_template):
			print "Cant file job template file", bt_opts.job_template
			sys.exit(1)

		# checking if extension is job template file extension is valid to detect type of scheduler
		if os.path.splitext(bt_opts.job_template)[1]  not in BUILDTEST_JOB_EXTENSION:
			print "Invalid file extension, must be one of the following extension", BUILDTEST_JOB_EXTENSION
			sys.exit(1)
	if bt_opts.submitjob is not None:
		submit_job_to_scheduler(bt_opts.submitjob)
		sys.exit(0)

	if bt_opts.sysyaml is not None:
		create_system_yaml(bt_opts.sysyaml)
	
	if bt_opts.ebyaml != None:
		raise NotImplementedError


	# when no argument is specified to -fc then output all yaml files
	if bt_opts.findconfig == "all": 
		find_all_yaml_configs()
		sys.exit(0)
	# find yaml configs by argument instead of reporting all yaml files
	elif bt_opts.findconfig is not None:
		find_yaml_configs_by_arg(bt_opts.findconfig)
		sys.exit(0)
	# report all buildtest generated test scripts
	if bt_opts.findtest == "all":
		find_all_tests()
		sys.exit(0)
	# find test by argument instead of all tests
	elif bt_opts.findtest is not None:
		find_tests_by_arg(bt_opts.findtest)
		sys.exit(0)


	#os.environ["BUILDTEST_LOGFILE"] = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")
	logdir =  BUILDTEST_LOGDIR
	logfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.log")

	logpath = os.path.join(logdir,logfile)
	
	# if log directory is not created do it automatically. Typically first run in buildtest will 
	# after git clone will run into this condition
	if not os.path.exists(logdir):
		os.makedirs(logdir)
		print "Creating Log directory: ", logdir

	#logging.basicConfig(filename=logfile)
	logger = logging.getLogger(logID)
	fh = logging.FileHandler(logpath)
        formatter = logging.Formatter('%(asctime)s [%(filename)s:%(lineno)s - %(funcName)5s() ] - [%(levelname)s] %(message)s')
 	fh.setFormatter(formatter)
	logger.addHandler(fh)
	logger.setLevel(logging.DEBUG)

	cmd = "env | grep BUILDTEST"
	ret = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	output = ret.communicate()[0]
	output = output.split("\n")

	for line in output:
		logger.debug(line)


	# if log directory is not created then create directory recursively
	if not os.path.exists(BUILDTEST_LOGDIR):
		os.makedirs(BUILDTEST_LOGDIR, 0755 )
		logger.warning("Directory not found: %s will create it", BUILDTEST_LOGDIR)

	# generate system pkg test
	if bt_opts.system is not None:
		if bt_opts.system == "all":
			systempkg = bt_opts.system
			logger.info("Generating all system package tests from YAML files in %s", os.path.join(BUILDTEST_SOURCEDIR,"system"))

			logdir = os.path.join(logdir,"system","all")
			systempkg_list = os.listdir(os.path.join(BUILDTEST_SOURCEDIR,"system"))

			logger.info("List of system packages to test: %s ", systempkg_list)

			for pkg in systempkg_list:
				generate_binary_test(bt_opts,pkg)
		else:
			systempkg = bt_opts.system
			logdir = os.path.join(logdir,"system",systempkg)
			generate_binary_test(bt_opts,systempkg)

		if not os.path.exists(logdir):
			os.makedirs(logdir,0755)
			logger.warning("Creating directory %s, to write log file", logdir)

		destpath = os.path.join(logdir,logfile)
		os.rename(logpath, destpath)
		logger.info("Moving log file from %s to %s", logpath, destpath)

		print "Writing Log file to:", destpath
		sys.exit(0)
	# when -s is specified
	if bt_opts.software is not None:
		software=bt_opts.software.split("/")


		if bt_opts.toolchain is None:
			toolchain="dummy/dummy".split("/")
		else:
	                toolchain=bt_opts.toolchain.split("/")

		appname=get_appname()
		appversion=get_appversion()
		tcname = get_toolchain_name()
		tcversion = get_toolchain_version()	

		logger.debug("Generating Test from EB Application")

		logger.debug("Software: %s", appname)
		logger.debug("Software Version: %s", appversion)
		logger.debug("Toolchain: %s", tcname)
		logger.debug("Toolchain Version: %s", tcversion)

		logger.debug("Checking if software: %s/%s exists",appname,appversion)


		# check that the software,toolchain match the easyconfig.
		ret=check_software_version_in_easyconfig(BUILDTEST_EASYCONFIGDIR)
		# generate_binary_test(software,toolchain,verbose)
	
		source_app_dir=os.path.join(BUILDTEST_SOURCEDIR,"ebapps",appname)

	        configdir=os.path.join(source_app_dir,"config")
	        codedir=os.path.join(source_app_dir,"code")
		os.environ["BUILDTEST_LOGDIR"]=os.path.join(BUILDTEST_ROOT,"log",appname,appversion,tcname,tcversion)
		logdir=os.environ["BUILDTEST_LOGDIR"]


		logger.debug("Source App Directory: %s",  source_app_dir)
		logger.debug("Config Directory: %s ", configdir)
		logger.debug("Code Directory: %s", codedir)

		generate_binary_test(bt_opts,None)

		# this generates all the compilation tests found in application directory ($BUILDTEST_SOURCEDIR/ebapps/<software>)
		recursive_gen_test(configdir,codedir)
	
		# if flag --testset is set, then 
		if bt_opts.testset is not  None:
			run_testset(bt_opts)
	
		if not os.path.exists(logdir):
			os.makedirs(logdir)

		# moving log file from $BUILDTEST_LOGDIR/buildtest_%H_%M_%d_%m_%Y.log to $BUILDTEST_LOGDIR/app/appver/tcname/tcver/buildtest_%H_%M_%d_%m_%Y.log
		os.rename(logpath, os.path.join(logdir,logfile))	
		logger.debug("Writing Log file to %s", os.path.join(logdir,logfile))
		
		print "Writing Log file: ", os.path.join(logdir,logfile)

if __name__ == "__main__":
        main()

