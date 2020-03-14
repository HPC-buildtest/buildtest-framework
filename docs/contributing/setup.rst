Getting Started
================

Contribution is not easy, so we created this document to describe how to get you setup
so you can contribute back and make everyone's life easier.

GitHub Account
--------------

If you don't have a GitHub account please `register <http://github.com/join>`_ your account

Fork the repo
--------------

First, you'll need to fork the repo https://github.com/HPC-buildtest/buildtest-framework

You might need to setup your SSH keys in your git profile if you are using ssh option for cloning. For more details on
setting up SSH keys in your profile, follow instruction found in
https://help.github.com/articles/connecting-to-github-with-ssh/

SSH key will help you pull and push to repository without requesting for password for every commit. Once you have forked the repo, clone your local repo::

  git clone git@github.com:YOUR\_GITHUB\_LOGIN/buildtest-framework.git


Adding Upstream Remote
-----------------------

First you need to add the ``upstream`` repo, to do this you can issue the
following::

 git remote add upstream git@github.com/HPC-buildtest/buildtest-framework.git

The ``upstream`` tag is used to sync changes from upstream repo to keep your
repo in sync before you contribute back.

Make sure you have set your user name and email set properly in git configuration. We don't want commits from
unknown users. This can be done by setting the following::

   git config user.name "First Last"
   git config user.email "abc@example.com"

For more details see `First Time Git Setup <https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup>`_

Sync your branch from upstream
-------------------------------

The ``devel`` from upstream will get Pull Requests from other contributors, in-order
to sync your forked repo with upstream, run the commands below::

 cd buildtest-framework
 git checkout devel
 git fetch upstream devel
 git pull upstream devel


Once the changes are pulled locally you can sync devel branch with your
fork as follows::

 git checkout devel
 git push origin devel


Repeat this same operation with ``master`` branch if you want to sync it with
upstream repo

Feature Branch
------------------

Please make sure to create a new branch when adding and new feature. Do not
push to ``master`` or ``devel`` branch on your fork or upstream.

Create a new branch from ``devel`` as follows::

  cd buildtest-framework
  git checkout devel
  git checkout -b featureX


Once you are ready to push to your fork repo do the following::

  git push origin featureX


Once the branch is created in your fork, you can create a PR for the ``devel``
branch for ``upstream`` repo (https://github.com/HPC-buildtest/buildtest-framework)

Pull Request Review
--------------------

Once you have submitted a Pull Request, please check the automated checks that are run for your PR to ensure checks are
passed. Please wait for buildtest maintainers to review your PR and provide feedback. If the reviewer requests
some changes, then you are requested to make changes and update the branch used for sending PR


Often times, you may start a feature branch and your PR get's out of sync with ``devel`` branch which may lead to conflicts,
this is a result of merging incoming PRs that may cause your PR to be out of date. The maintainers will check for this during
PR review or GitHub will report file conflicts during merge.

Syncing your feature branch with devel is out of scope for this documentation, however you can use the steps below
as a *guide* when you run into this issue.

Anyhow, you may want to take the steps to first sync devel branch and then selectively rebase or merge ``devel`` into your
feature branch.

First go to ``devel`` branch and fetch changes from upstream::

    git checkout devel
    git fetch upstream devel

Note you shouldn't be making any changes to your local ``devel`` branch, if ``git fetch`` was successful you can merge your
``devel`` with upstream as follows::

    git merge upstream/devel

Next, navigate to your feature branch and sync feature changes with devel::

    git checkout <feature-branch>
    git merge devel

.. Note:: Running above command will sync your feature branch with ``devel`` but you may have some file conflicts depending on files changed during PR. You will need to resolve them manually before pushing your changes

Instead of merge from ``devel`` you can rebase your commits interactively when syncing with ``devel``. This can be done by running::

    git rebase -i devel

Once you have synced your branch push your changes and check if file conflicts are resolved in your Pull Request::

    git push origin <feature-branch>

