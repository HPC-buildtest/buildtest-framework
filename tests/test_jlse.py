import os
import pytest
import socket
from buildtest.cli.build import BuildTest
from buildtest.cli.compilers import BuildtestCompilers
from buildtest.config import SiteConfiguration
from buildtest.system import BuildTestSystem

hostname = socket.getfqdn()


def test_jlse():

    if not hostname.endswith("alcf.anl.gov"):
        pytest.skip("Test runs only on JLSE Login Nodes with domain name alcf.anl.gov")

    here = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(here, "settings", "jlse.yml")
    system = BuildTestSystem()
    system.check()

    bc = SiteConfiguration(settings_file)
    bc.get_current_system()
    bc.validate()

    buildspec_files = os.path.join(here, "examples", "jlse", "hostname.yml")

    cmd = BuildTest(
        configuration=bc, buildspecs=[buildspec_files], buildtest_system=system
    )
    cmd.build()

    # testing buildtest config compilers find
    bc = BuildtestCompilers(configuration=bc)
    bc.find_compilers()
