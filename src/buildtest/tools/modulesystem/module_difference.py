import os, sys
from buildtest.tools.file import is_dir, string_in_file

def get_module_list_by_tree(mod_tree):
    """The method returns a list of module file paths from a module tree.

    :param mod_tree: root of module tree
    :type mod_tree: str, required
    :return: list of absolute path to module files
    :rtype: list
    """

    modulefiles = []

    is_dir(mod_tree)
    for root, dirs, files in os.walk(mod_tree):
        for fname in files:
            if fname.endswith(".lua") or string_in_file("#%Module",os.path.join(root,fname)):
                modulefiles.append(os.path.join(root,fname))

    return modulefiles

def diff_trees(args_trees):
    """This method display difference between module trees by presenting
    modules found in tree 1 and tree 2. This method invokes
    **get_module_list_by_tree()** to get module files from both trees.
    This implements command ``buildtest module --diff-trees <tree1>,<tree2>``

    :param args_trees: root of two module trees separated by comma
    :type args_trees: str, required
    :rtype: 1 if comma a is not found
    """

    # no comma found between two trees
    if args_trees.find(",") == -1:
        print ("Usage: --diff-trees /path/to/tree1,/path/to/tree2")
        sys.exit(1)
    else:
        id_x = args_trees.find(",")
        tree1 = args_trees[0:id_x]
        tree2 = args_trees[id_x+1:len(args_trees)]

        is_dir(tree1)
        is_dir(tree2)

        modlist1 = []
        modlist2 = []

        list1 = get_module_list_by_tree(tree1)
        list2 = get_module_list_by_tree(tree2)

        # strip full path, just get a list module file in format app/version
        for fname in list1:
            name = os.path.basename(os.path.dirname(fname))
            # strip out any file extension (.lua)
            ver = os.path.basename(os.path.splitext(fname)[0])
            modlist1.append(os.path.join(name,ver))

        for fname in list2:
            name = os.path.basename(os.path.dirname(fname))
            # strip out any file extension (.lua)
            ver = os.path.basename(os.path.splitext(fname)[0])
            modlist2.append(os.path.join(name,ver))

        # convert list into set and do symmetric difference between two sets

        diff_set =  set(modlist1).symmetric_difference(set(modlist2))
        if not diff_set:
            print ("No difference found between module tree: ", tree1, " and module tree: ", tree2)
        # print difference between two sets by printing module file and stating  FOUND or NOTFOUND in the appropriate columns for Module Tree 1 or 2
        else:
            print ("\t\t\t Comparing Module Trees for differences in module files")
            print ("\t\t\t -------------------------------------------------------")

            print
            print ("Module Tree 1: ", tree1)
            print ("Module Tree 2: ", tree2)
            print
            print ("ID       |     Module                                                   |   Module Tree 1    |   Module Tree 2")
            print ("---------|--------------------------------------------------------------|--------------------|----------------------")

            count = 1
            # print difference set
            for i in diff_set:
                module_in_tree = ""
                value1 = "NOT FOUND"
                value2 = "NOT FOUND"
                # finding which module tree the module belongs
                if i in modlist1:
                    module_in_tree = tree1
                if i in modlist2:
                    module_in_tree = tree2

                if module_in_tree == tree1:
                    value1 = "FOUND"

                if module_in_tree == tree2:
                    value2 = "FOUND"


                print ((str(count) + "\t |").expandtabs(8), (i + "\t |").expandtabs(60) , (value1 + "\t |").expandtabs(18), value2)
                count = count + 1
