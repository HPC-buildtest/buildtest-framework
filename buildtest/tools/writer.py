import logging
import json
import os
import sys
import stat

from buildtest.tools.config import logID, BUILDTEST_BUILD_HISTORY
from buildtest.tools.buildsystem.status import get_total_build_ids
from buildtest.tools.system import BuildTestCommand


def write_test(dict, verbose):
    """Method responsible for writing test script."""

    logger = logging.getLogger(logID)

    build_id = get_total_build_ids()

    fd = open(dict["testpath"], "w")
    logger.info(f"Opening Test File for Writing: {dict['testpath']}")

    if verbose >= 2:
        print(f"{json.dump(dict,sys.stdout,indent=4)}")

    for key, val in dict.items():
        # skip key testpath, this key is responsible for opening the file for writing purpose.
        # any value that is empty skip to next key.
        if key == "testpath":
            continue
        if val is None:
            continue
        fd.write("\n".join(val))
        fd.write("\n")

    fd.close()

    os.chmod(
        dict["testpath"],
        stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH,
    )

    if verbose >= 1:
        print(f"Changing permission to 755 for test: {dict['testpath']}")

    if verbose >= 2:
        query = BuildTestCommand()
        cmd = f"cat {dict['testpath']}"
        query.execute(cmd)
        test_output = query.get_output().splitlines()
        print("{:_<80}".format(""))
        for line in test_output:
            print(line)
        print("{:_<80}".format(""))

    BUILDTEST_BUILD_HISTORY[build_id]["TESTS"].append(dict["testpath"])
