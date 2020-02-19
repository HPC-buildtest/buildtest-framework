"""
This module implements methods for querying status details of previous
builds by buildtest. This includes a summary of all builds, number of test and
command executed along with build ID. The build ID can be used to retrieve log files
and test scripts that were generated.
"""

import json
import os
import subprocess
from datetime import datetime
from buildtest.tools.config import config_opts, BUILDTEST_BUILD_LOGFILE
from buildtest.tools.file import create_dir


def show_status_report(args=None):
    """
    This method displays history of builds conducted by buildtest. This method
    implements command ``buildtest build report``.

    :param args: command line arguments passed to buildtest
    :type args: dict, required
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()

    print(
        "{:3} | {:<20} | {:<15} | {:<60} ".format(
            "ID", "Build Time", "Number of Tests", "Command"
        )
    )

    print("{:-<120}".format(""))
    count = 0

    for build_id in content["build"].keys():

        print(
            "{:3} | {:<20} | {:<15} | {:<60} ".format(
                count,
                content["build"][build_id]["BUILD_TIME"],
                content["build"][build_id]["TESTCOUNT"],
                content["build"][build_id]["CMD"],
                content["build"][build_id]["LOGFILE"],
            )
        )
        count += 1


def show_status_log(args):
    """This method opens log file using "less" by reading build.json
    and fetching log file based on build id. This method implements
    ``buildtest status log``.

    :param args: command arguments passed to buildtest
    :type args: dict, required
    """
    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()

    logfile = content["build"][str(args.id)]["LOGFILE"]
    query = f"less {logfile}"
    os.system(query)


def show_status_test(args):
    """ This method list tests generated from a build ID. This method
    implements ``buildtest status test``

    :param args: command line argument passed to buildtest
    :type args: dict, required
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()

    tests = content["build"][str(args.id)]["TESTS"]
    [print(test) for test in tests]


def run_tests(args):
    """This method actually runs the test and display test summary"""

    fd1 = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd1)
    fd1.close()

    tests = content["build"][str(args.id)]["TESTS"]

    # all tests are in same directory, retrieving parent directory of test
    test_dir = content["build"][str(args.id)]["TESTDIR"]

    runfile = datetime.now().strftime("buildtest_%H_%M_%d_%m_%Y.run")
    run_output_file = os.path.join(test_dir, "run", runfile)
    create_dir(os.path.join(test_dir, "run"))
    fd = open(run_output_file, "w")
    count_test = len(tests)
    passed_test = 0
    failed_test = 0

    for test in tests:
        ret = subprocess.Popen(
            test, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
        output = ret.communicate()[0].decode("utf-8")

        ret_code = ret.returncode
        fd.write("Test Name:" + test + "\n")
        fd.write("Return Code: " + str(ret_code) + "\n")
        fd.write("---------- START OF TEST OUTPUT ---------------- \n")
        fd.write(output)
        fd.write("------------ END OF TEST OUTPUT ---------------- \n")

        if ret_code == 0:
            passed_test += 1
        else:
            failed_test += 1

    print(f"Running All Tests from Test Directory: {test_dir}")
    print
    print
    print("==============================================================")
    print("                         Test summary                         ")
    print(f"Executed {count_test} tests")
    print(f"Passed Tests: {passed_test} Percentage: {passed_test*100/count_test}%")
    print(f"Failed Tests: {failed_test} Percentage: {failed_test*100/count_test}%")
    print
    print
    print("Writing results to " + run_output_file)
    fd.close()


def get_build_ids():
    """Return a list of build ids. This can be retrieved by getting length
    of "build:" key and pass it to range() method to return a list. Build IDs
    start from 0. This method is used as choice field in add_argument() method

    :return: return a list of numbers  that represent build id
    :rtype: list
    """
    if not os.path.exists(BUILDTEST_BUILD_LOGFILE):
        return []

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()
    total_records = len(content["build"])
    return range(total_records)


def get_total_build_ids():
    """Return a total count of build ids. This can be retrieved by getting length
    of "build:" key. Build IDs start from 0.

    :return: return a list of numbers  that represent build id
    :rtype: list
    """

    fd = open(BUILDTEST_BUILD_LOGFILE, "r")
    content = json.load(fd)
    fd.close()
    total_records = len(content["build"])
    return total_records
