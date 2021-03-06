import os
import pytest
from buildtest.cli.cdash import cdash_cmd
from buildtest.config import SiteConfiguration

configuration = SiteConfiguration()
configuration.get_current_system()
configuration.validate()


def test_cdash_view():
    class args:
        cdash = "view"
        url = None

    cdash_cmd(args=args, default_configuration=configuration, open_browser=False)


def test_cdash_upload():
    class args:
        cdash = "upload"
        buildname = "TESTING"
        site = None
        report_file = None

    cdash_cmd(args, default_configuration=configuration)


def test_cdash_upload_exceptions():
    class args:
        cdash = "upload"
        buildname = None
        site = None
        report_file = None

    # a buildname must be specified, a None will result in error
    with pytest.raises(SystemExit):
        cdash_cmd(args, default_configuration=configuration)

    here = os.path.dirname(__file__)

    bc = SiteConfiguration(
        os.path.abspath(os.path.join(here, "cdash_examples", "invalid_url.yml"))
    )
    bc.get_current_system()

    class args:
        cdash = "upload"
        buildname = "DEMO"
        site = None
        report_file = None

    # in configuration file we have invalid url to CDASH server
    with pytest.raises(SystemExit):
        cdash_cmd(args, default_configuration=bc)

    bc = SiteConfiguration(
        os.path.abspath(os.path.join(here, "cdash_examples", "invalid_project.yml"))
    )
    bc.get_current_system()

    class args:
        cdash = "upload"
        buildname = "DEMO"
        site = None
        report_file = None

    # in configuration file we have invalid project name in CDASH
    with pytest.raises(SystemExit):
        cdash_cmd(args, default_configuration=bc)
