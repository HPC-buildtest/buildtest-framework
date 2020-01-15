| |license| |docs| |travis| |codecov| |coverall| |slack| |core_infrastructure| |tags| |forks| |issues| |contributors| |stars| |watchers|

.. |docs| image:: https://readthedocs.org/projects/buildtest/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://buildtest.readthedocs.io/en/latest/?badge=latest

.. |slack| image:: http://hpcbuildtest.herokuapp.com/badge.svg
.. |license| image:: https://img.shields.io/github/license/HPC-buildtest/buildtest-framework.svg
.. |core_infrastructure| image:: https://bestpractices.coreinfrastructure.org/projects/3469/badge
.. |tags| image:: https://img.shields.io/github/v/tag/HPC-buildtest/buildtest-framework.svg
.. |forks| image:: https://img.shields.io/github/forks/HPC-buildtest/buildtest-framework.svg
.. |issues| image:: https://img.shields.io/github/issues/HPC-buildtest/buildtest-framework.svg
.. |contributors| image:: https://img.shields.io/github/contributors/HPC-buildtest/buildtest-framework.svg
.. |stars| image:: https://img.shields.io/github/stars/HPC-buildtest/buildtest-framework.svg
.. |watchers| image:: https://img.shields.io/github/watchers/HPC-buildtest/buildtest-framework.svg
.. |codecov| image:: https://codecov.io/gh/HPC-buildtest/buildtest-framework/branch/devel/graph/badge.svg
    :target: https://codecov.io/gh/HPC-buildtest/buildtest-framework
.. |coverall| image:: https://coveralls.io/repos/github/HPC-buildtest/buildtest-framework/badge.svg?branch=devel
    :target: https://coveralls.io/github/HPC-buildtest/buildtest-framework?branch=devel

.. |travis| image:: https://travis-ci.com/HPC-buildtest/buildtest-framework.svg?branch=devel
    :target: https://travis-ci.com/HPC-buildtest/buildtest-framework

buildtest
---------

buildtest is a software stack testing framework that automates test creation and execution to help HPC facilities to
better support and validate their software stack. buildtest is a central repository with collection of tests for all
scientific software that is installed in HPC. buildtest makes use of `YAML <https://yaml.org/>`_ configuration to write
test configuration that is reusable and adaptable to other HPC sites.

To get started with buildtest see `Setup Section <https://buildtest.readthedocs.io/en/latest/setup.html>`_

Why buildtest?
---------------

Read https://buildtest.readthedocs.io/en/latest/what_is_buildtest.html to understand why we need buildtest and what we
are trying to solve.

Documentation
-------------

buildtest `documentation <http://buildtest.readthedocs.io/en/latest/>`_  is your source for getting help with buildtest.
If you get stuck check out the `current issues <https://github.com/HPC-buildtest/buildtest-framework/issues>`_ to see
if you face similar issue. If all else fails please create a ticket.

Source Code
------------

buildtest source code is under ``src`` directory found in the root of this repository, with the exception of
`buildtest <https://github.com/HPC-buildtest/buildtest-framework/blob/master/buildtest>`_ which is in the root of this
repo.

The documentation  is under ``docs`` which consist of ``Makefile`` to build the sphinx project along with documentation
pages in RestructuredText and test scripts for documentation under ``docs/scripts``

Slack
------

Click the `Join Slack Channel <https://hpcbuildtest.herokuapp.com/>`_ to get in touch with the buildtest community.
If you already have an account then access the Slack Channel `here  <https://hpcbuildtest.slack.com>`_


Contributing Back
-------------------

We would love to get your contribution, if you are not sure check out the
`Contribution Guide <https://buildtest.readthedocs.io/en/latest/contributing.html>`_ to get started.


Author
-------

buildtest was founded by `Shahzeb Siddiqui <https://github.com/shahzebsiddiqui>`_ on Feb 24th 2017 see
`first commit <https://github.com/HPC-buildtest/buildtest-framework/commit/902237c1a3707e00b32da5830d3f8abc92ecf296>`_

Special thanks to all the  `contributors <https://github.com/HPC-buildtest/buildtest-framework/graphs/contributors>`_
that helped contribute to buildtest

LICENSE
--------

buildtest is released under the MIT License. See
`LICENSE <https://github.com/HPC-buildtest/buildtest-framework/blob/master/LICENSE>`_ for more details
