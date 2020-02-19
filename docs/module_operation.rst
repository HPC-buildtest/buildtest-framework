Module Operation
==================

.. contents::
   :backlinks: none

Module Options (``buildtest module --help``)
----------------------------------------------

.. program-output:: cat docgen/buildtest_module_-h.txt

.. _buildtest_module_list:

Module List (``buildtest module list``)
-------------------------------------------

.. program-output:: cat docgen/buildtest_module_list_-h.txt

buildtest can report list of all modules (full Canonical Name) and absolute path to module file by searching all
module trees defined by **BUILDTEST_MODULEPATH**. buildtest comes with a default configuration defined in settings.yml
as follows::

    module:
      list:
        exclude_version_files: true
        filter:
          include: []
        querylimit: -1


Each of these configuration can be overridden by passing them via command line. By default, buildtest will exclude version
files from the output. The version files are **.version**, **.modulerc** or **.modulerc.lua** files found in same directory
where module files reside. This is controlled by setting ``exclude_version_files: true``. If you set ``exclude_version_files: false``
then buildtest will report version files in output if found at your site. You can override this setting by passing
option ``--exclude-version-files``.

To limit output of query you can set ``querylimit`` to a positive value. A negative value or 0 will result in all modules
to be printed. You can override this option by passing ``--querylimit`` via command line.

If you are interested in filter output by module full name you can use the option ``--filter-include`` or use the configuration
file. For example, you are interested in reporting all ``GCC``, ``Python`` and ``zlib`` modules you can set this in your
configuration as follows::

    module:
      list:
        filter:
          include: [GCC, Python, zlib]

Shown below is an example of filtered output by modules

.. program-output:: cat docgen/buildtest-module-list-filter.txt

Shown below is an example of restricting output by using ``--querylimit``

.. program-output:: cat docgen/buildtest-module-list-limit.txt

The behavior of ``buildtest module list`` will be altered based on how buildtest retrieves spider record. See :ref:``configuring_spider`
for more details. If ``spider_view: all`` then ``buidtest module list`` will return modules from all sub-trees that are
a result which may not have been defined in ``BUILDTEST_MODULEPATH``.

Difference Between Module Trees (``buildtest module --diff-trees``)
--------------------------------------------------------------------

buildtest can report differences between two module trees that can be useful if you deploy your software in a
**stage/prod** module tree and you want to keep these trees in sync.

If your HPC site builds software stack for each architecture and your environment is
heterogeneous then ``--diff-trees`` option will be helpful.


buildtest takes two trees as argument in the form of ``buildtest --diff-tree tree1,tree2``
where trees are separated by a comma. The tree must point to the root of the module tree in your
system and buildtest will walk through the entire tree. We expect this operation to be quick
given that the module tree is on the order of few thousand module files which is a reasonable
count of module files in a large HPC facility.

.. program-output:: cat docgen/module-diff-trees.txt

If your site supports multiple architecture and you want to find difference
between the stacks then you will find ``--diff-trees`` to be handy. If the
stacks are same you will see the following message

.. program-output:: cat docgen/module-diff-trees-same.txt


Module Load Testing (``buildtest module loadtest``)
--------------------------------------------------------------

.. program-output:: cat docgen/buildtest_module_loadtest_-h.txt

buildtest provides feature to test ``module load`` functionality on all module files
in a module tree. This assumes you have the module tree in ``MODULEPATH`` in order
for ``module`` command to work properly.

To use this feature specify the appropriate module tree for parameter ``BUILDTEST_MODULEPATH`` in
``settings.yml`` or via environment variable. To use this feature you need to
use ``buildtest module loadtest``

To demonstrate let's kick off a module load test as shown below.

.. program-output:: head -14 docgen/moduleload-test.txt

buildtest will attempt to run ``module load`` against each module to verify modules are working properly.

Tweaking module loadtest behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The buildtest configuration (**settings.yml**) related to module loadtest, comes with a default set of options as shown below::

    module:
      loadtest:
        login: false
        numtest: -1
        purge_modules: true


If you want to run each test in a login shell consider setting ``login: true`` in configuration or via ``--login`` on
the command line. buildtest will insert ``module purge`` before loading the modules, this can be changed by using flag ``--purge-modules`` on
command line to enable purging modules. Alternatively you can configure this in your buildtest configuration ``purge_modules``.
Setting ``purge_modules: false`` will cause buildtest to **NOT** purge the modules before loading modules. Options passed
by command line will override configuration setting.


Shown below we test modules in a login shell ``--login`` and restrict test to 5 entries by setting ``--numtest 5``.

.. program-output:: cat docgen/moduleload-test-login.txt

You may specify additional module trees using ``BUILDTEST_MODULEPATH`` for module testing. If you want to test all
modules that were detected by spider utility, you can set ``spider_view=all`` in your configuration. See :ref:`configuring_spider`
This will test all modules retrieved by spider utility.

.. _module_collection:

Module Collection Operation (``buildtest module collection``)
-------------------------------------------------------------

buildtest keeps track of its own module collection which is stored in
``BUILDTEST_ROOT/vars/collection.json``. This file is  maintained
by buildtest when using ``buildtest module collection`` commands.

buildtest supports adding, removing, updating and listing module collection.
This is synonymous to using user collection from Lmod (i.e ``module save <collection>``).

Shown below is a usage of module collection options in buildtest.

.. program-output:: cat docgen/buildtest_module_collection_-h.txt


Adding a module collection (``buildtest module collection -a``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add a module collection, just load modules in your shell environment and
run the following::

    $ buildtest module collection -a

Shown below is an example output

.. program-output:: cat docgen/module_collection_add.txt

Once modules are added, you may build a test using a module collection using the
option ``buildtest build --module-collection <ID>``. The <ID> is the index number to reference
the module collection. For more information on buildtest with module collection see :ref:`build_with_module_collection`


List all module collection (``buildtest module collection -l``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest can report a list of all module collections that is easy to interpret
as pose to reading a json file. To get a list of all module collection run the following::

    $ buildtest module collection -l

Shown below is an example output

.. program-output:: cat docgen/module_collection_list_add.txt

If the collection is empty the output will be the following

.. program-output:: cat docgen/module_collection_list_empty.txt


Removing a module collection (``buildtest module collection -r <ID>``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To remove a module collection, you will need to specify the index number to the ``-r`` option.
One can check the module collection index by listing module collection using **buildtest module collection -l**.

In this example we will remove module collection **0** as shown below.

.. program-output:: cat docgen/module_collection_remove.txt

buildtest will remove the index and update the json file. Note all existing module collection
will update their collection index depending what index number was removed.

Updating a module collection (``buildtest module collection -u <ID>``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To update a module collection you will need the index number of module
collection and use the ``--update <INDEX>`` to update the module collection.

Shown below is an example where we update collection index **0**

.. program-output:: cat scripts/buildtest-module-collection-update.txt

Delete all module collections (``buildtest module collection --clear``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to delete all module collections you can run

.. program-output:: cat docgen/buildtest_module_collection_--clear.txt


This will remove all module collection index from the internal database.

Check Module Collection (``buildtest module collection --check``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

buildtest provides a mechanism to test if your module collection can be loaded properly before you use them with
building your test. Modules loaded at one given time may break in future if certain environment change or name change
of module occurs. buildtest will conduct a ``module load`` test against all collections and report for any bugs.

To use this option use the ``--check`` option.

If everything is all well you should get the following message

.. program-output:: cat docgen/module_collection_check.txt

If you encounter an error you will get a message as follows::

    $ buildtest module collection --check
    The following module collection failed to load:
    Collection: 0 - module load GCCcore/9.3.0
    Collection[0] = ['GCCcore/9.3.0', 'bzip2/1.0.8-GCCcore-8.3.0', 'zlib/1.2.11-GCCcore-8.3.0', 'ncurses/6.1-GCCcore-8.3.0', 'libreadline/8.0-GCCcore-8.3.0', 'Tcl/8.6.9-GCCcore-8.3.0', 'SQLite/3.29.0-GCCcore-8.3.0', 'XZ/5.2.4-GCCcore-8.3.0', 'GMP/6.1.2-GCCcore-8.3.0', 'libffi/3.2.1-GCCcore-8.3.0', 'Python/3.7.4-GCCcore-8.3.0']

buildtest will attempt to load each module individually as pose to loading all of them in a single command. This means the above collection
will run the following::

    module load GCCcore/9.3.0
    module load bzip2/1.0.8-GCCcore-8.3.0
    ...

To fix a module collection issue, try removing the module collection or update the collection with a new set of modules.

If you don't have any module collection and you run ``--check`` option you will get the following message::

    $  buildtest module collection --check
    No modules collection found. Please add a module collection before running check.

.. _module_tree_operation:

Module Trees Operation (``buildtest module tree``)
---------------------------------------------------

buildtest supports adding, removing, listing, and setting module trees. Internally, buildtest
is modifying BUILDTEST_MODULEPATH which is synonymous to MODULEPATH though,
buildtest makes use of ``BUILDTEST_MODULEPATH`` when querying modules from ``spider``
command.

At your site, you will need to alter BUILDTEST_MODULEPATH to the root of your module trees where
software stack is present.

By default, BUILDTEST_MODULEPATH is set to an empty list ``[]`` in configuration
file ``$HOME/.buildtest/settings.yml``. In this case, BUILDTEST_MODULEPATH will read
from ``MODULEPATH``.

One could edit the configuration file manually; however, it's preferable to use
``buildtest module tree`` commands to alter BUILDTEST_MODULEPATH to avoid syntax error in
configure file which can break buildtest functionality.

Shown below is a usage of ``buildtest module tree`` command.

.. program-output:: cat docgen/buildtest_module_tree_-h.txt


Listing Module Trees (``buildtest module tree -l``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list the module trees in buildtest you can run ``buildtest module tree -l``
which shows one module tree per line

.. program-output:: cat docgen/buildtest_module_tree_-l.txt

For this run, ``BUILDTEST_MODULEPATH`` is not set in configuration file so it is
reading from ``MODULEPATH``

.. code-block:: console

    $ cat ~/.buildtest/settings.yml  | grep -i BUILDTEST_MODULEPATH
    BUILDTEST_MODULEPATH: []

Adding a Module Tree (``buildtest module tree -a``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add new module tree through command line using ``buildtest module
tree -a /path/to/tree`` which will update the configuration file. Use this option
to add software stack into buildtest environment for testing purposes.

.. program-output:: cat docgen/add_module_tree.txt


Removing a Module Tree (``buildtest module tree -r``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly you can remove module tree from your configuration via ``buildtest module tree -r /path/to/tree``.
Use this option to remove a software stack from buildtest environment.

.. program-output:: cat docgen/remove_module_tree.txt

Setting a Module Tree (``buildtest module tree -s``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can set BUILDTEST_MODULEPATH to a tree which will override current value. For instance
you have the following module trees in buildtest

.. program-output:: cat docgen/default_module_tree.txt

Now if we want to set BUILDTEST_MODULEPATH to a tree, let's assume **/usr/share/lmod/lmod/modulefiles/Core** we
can do that as follows

.. program-output:: cat docgen/set_module_tree.txt

Next we can check the list of module trees by issuing the following

.. program-output:: cat docgen/set_module_tree_view.txt


Report Easybuild Modules (``buildtest module --easybuild``)
------------------------------------------------------------

buildtest can detect modules that are built by `Easybuild <https://easybuild.readthedocs.io/en/latest/>`_.
An easybuild module will contain a string in module file as follows::

    Built with EasyBuild version 3.7.1

buildtest will check all module trees defined by ``BUILDTEST_MODULEPATH`` and search
for string without the version number. To enable this feature use
``buildtest module --easybuild`` or short option ``buildtest module -eb``.

Shown below is the output of easybuild retrieval.

.. program-output:: cat docgen/easybuild_modules.txt

Report Spack Modules (``buildtest module --spack``)
----------------------------------------------------

buildtest can detect `Spack <https://spack.readthedocs.io/en/latest/>`_ modules. A
spack module has a string to denote this module was created by spack with timestamp of module
creation. Shown below is an example::

    Module file created by spack (https://github.com/spack/spack) on 2019-04-11 11:38:31.191604


buildtest will search for string ``Module file created by spack`` in modulefile. buildtest
will run this for all modules in module trees defined by ``BUILDTEST_MODULEPATH``.


.. program-output:: cat docgen/spack_modules.txt

List All Parent Modules (``buildtest module --list-all-parents``)
-----------------------------------------------------------------------

buildtest will read ``BUILDTEST_ROOT/vars/spider.json`` when searching all parent modules.

buildtest can retieve all parent modules from all module trees defined in BUILDTEST_MODULEPATH.
This can be useful for users and administrators to find all sub-trees (**MODULEPATH**) that are
defined in module files.

To retrieve all parent modules run ``buildtest module --list-all-parents`` as shown below

.. program-output:: cat docgen/buildtest-list-all-parents.txt

buildtest will return the module full name and path to module file.

.. Note:: buildtest is unable to differentiate two modules with same full canonical name (**N/V**) when traversing
          spider record. The spider key ``parent`` only contains full name and it doesn't contain abspath to
          modulefile.

Parent Modules (``buildtest module --module-deps``)
-----------------------------------------------------

Parent modules are modules that set **MODULEPATH** in the modulefile. This
technique is used in **Hierarchical Module Naming Scheme** where modules like
compilers, mpi, numlibs expose new module trees. These modules are called
parent modules.

buildtest can report list of modules depended on a parent module. First,
buildtest will seek out all parent module from file
``BUILDTEST_ROOT/vars/spider.json``.

To seek out modules that depend on parent modules use the option
``buildtest module --module-deps`` or short option ``buildtest module -d``.

Shown below is a sample run for parent module ``GCCcore/8.1.0``. buildtest
will report the content of the module file and list of modules that are
depended upon the module.

.. program-output:: cat docgen/parent_modules.txt

buildtest will auto-populate the choice field for option ``-d`` that is a list of parent modules. If you
are unsure which parent module to choose, just press TAB to get a list of parent modules.



