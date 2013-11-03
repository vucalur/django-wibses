****************************************
Wibses
****************************************

Wibses stands for Web Interface for Building SEmantic Scripts. (semi acronym)


============
Contributing
============

Git Workflow
============

- We use simplest possible rebase workflow based on `this <http://git-scm.com/book/en/Git-Branching-Rebasing>`_.  
- Reading whole `Chapter 3 <http://git-scm.com/book/en/Git-Branching>`_ is strongly encouraged.
- Do not even try invoking ``$ git pull`` or committing 3-way-merge crap like ``Merge branch 'master' of github.com: blah blah blah`` :-)
  3-way-merges obfuscate history and screw annotations in IDE - Existing code that you are merging in gets annotated with your name, even if you aren't the author.
  
Cheatsheet - Rebase Workflow
***********

Plain old local commmits of your work to master branch:
------------------------------

.. code-block:: bash

  $ # git pull    # !!!!!!!!!!!   DO NOT EVEN TRY   !!!!!!!!!!!
  $ git fetch   # Keep up with recent changes before begining work.
  ...
  $ git commit -m '[#123] Implemented a mechanism to make "blah blah blah" sound wise'  # commit your work

Some advice:

- Use ``git commit --amend``. It's more reliable and faster than local history in IDE.
- If you have a tendency to break down single unit of work into multiple commits locally, remember to squash them before submmiting to repo.

Synchronizing with repo:
----------------------

.. code-block:: bash

  $ git checkout master   # make sure you are on master branch
  $ git fetch  # update origin/master with the latest changes from repo. It's safe = No conflicts here, since origin/master is a remote branch.
  $ git rebase origin/master    # Place your local commits on top of commits from repo, that you just fetched. If you're lucky this will be a fast-forward. If not (changes in the same places), get ready for a merge:
     # Supposing you have a merge:
        # 1. Resolve conflicts by editing conflicted files
        $ git add <<conflicted_files_here__space_separated>>    # 2. Mark conflicted files as resolved. In git you do that by by staging those files.
        $ git rebase --continue  # 3.
        
  # At this point you have local history in-sync with repo
  # Now you can submit your code with plain old push:
  $ git push

For more information what's happening here, refer to `Rebasing subchapter of ProGit <http://git-scm.com/book/en/Git-Branching-Rebasing>`_.


Indentation
============

- Project is developed under PyCharm 3.X.
- Make sure you are using `JetBrains Codestyle <https://github.com/vucalur/JetBrains-Codestyle>`_ to indent your code.
- Some files should not be formatted - check what you're commiting.
- Warning: PyCharm's code formatter tends to leave CoffeeScript code unindented or screw CS indentation at all. Beware.



Code Analysis
============

- lint your (Coffee|Java)Script. Linting is done in default grunt task:
.. code-block:: bash

    $ grunt
    
- Feel free to ask for a code-review

CI
============

- Make sure both e2e & unit tests pass. They will be executed by: ``$ grunt`` or ``$ grunt test`` or ``$ karma start``

    
Commit messages
============

- Be precise, concise and meaningful
- Pick up a tense you like. It doesn't have to be a sentence at all, as long as above condition holds :)
- Whenever there is a ticket created for what you are working on, reference it in a commit message, like:
..

    [#123] Implemented a mechanism to make "blah blah blah" sound wise

============
Developer's Cheatsheet
============

Installing beta/RC dependency version with bower (work-around-ish way)
===================
.. code-block:: bash

    $ bower install angular-cookies --save

|  It will in fact put the latest *stable* version in bower.json, even if you select otherwise, hence next steps:
|  Then edit bower.json and manually change version of the new dependency (bower seems to have problems with beta, RC releases).

.. code-block:: bash

    $ bower update  # to actually fetch manually changed version

.. code-block:: bash

    $ grunt bower-install
    
The last one sometimes has to be invoked a couple of times to inject all stuff properly.
