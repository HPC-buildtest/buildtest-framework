import os

from buildtest.config import load_settings, check_settings
from buildtest.menu import BuildTestParser
from buildtest.menu.repo import validate_repos
from buildtest.menu.build import func_build_subcmd
from buildtest.system import BuildTestSystem
from buildtest.log import init_logfile, streamlog

# column width for linewrap for argparse library
os.environ["COLUMNS"] = "120"


def main():
    """Entry point to buildtest."""

    buildtest_logfile = "buildtest.log"
    if os.path.exists(buildtest_logfile):
        os.remove(buildtest_logfile)

    logger = init_logfile(buildtest_logfile)
    logger.info("Starting buildtest log")

    # Create a build test system, and check requirements
    BuildTestSystem()

    validate_repos()

    parser = BuildTestParser()
    args = parser.parse_options()

    if args.debug:
        streamlog(args.debug)

    # invoking load_settings will attempt to initialize buildtest settings and
    # load the schema
    buildtest_configuration = load_settings()
    check_settings()

    if args.subcommands == "build":
        func_build_subcmd(args, buildtest_configuration)
    else:
        if args.subcommands and args.func:
            args.func(args)


if __name__ == "__main__":
    main()
