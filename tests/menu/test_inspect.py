from buildtest.menu.inspect import get_all_ids, func_inspect


def test_inspect_ids():

    test_ids = get_all_ids()
    # return should be a list of test ids
    assert isinstance(test_ids, dict)

    # ensure there is atleast one test ID in report.json
    assert len(test_ids.keys()) >= 1
    print(test_ids)

def test_buildtest_inspect_list():
    class args:
        subcommands = "list"

    func_inspect(args)

def test_buildtest_inspect_name():

    test_ids = get_all_ids()
    test_name = None

    for identifier, name in test_ids.items():
        test_name = name
        break

    class args:
        subcommands = "name"
        name = [test_name]

    print(f"Querying test names: {args.name}")
    func_inspect(args)

def test_buildtest_inspect_id():

    test_ids = get_all_ids()

    identifier = list(test_ids.keys())[0]

    class args:
        subcommands = "id"
        id = [identifier]

    print(f"Querying test identifier: {args.id}")
    func_inspect(args)

