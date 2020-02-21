from buildtest.tools.modulesystem.collection import (
    add_collection,
    list_collection,
    clear_module_collection,
    remove_collection,
    get_collection_length,
    check_module_collection,
    get_buildtest_module_collection,
)


def test_module_collection_add():
    add_collection()
    list_collection()


def test_remove_module_collection():
    add_collection()
    list_collection()
    remove_collection(0)


def test_clear_module_collection():
    clear_module_collection()


def test_get_module_collection():
    clear_module_collection()
    add_collection()
    module_list = get_buildtest_module_collection(0)
    print(module_list)
    assert len(module_list) > 0


def test_collection_length_when_empty():
    clear_module_collection()
    assert 0 == get_collection_length()

    # listing module collection after clearing collection
    list_collection()

    # check all module collection when empty list
    check_module_collection()
