|

The GMU PyPi Template
---------------------

https://www.thegmu.com/

:Authors: Mybrid Wonderful, Gregg Yearwood
:Date: 11/03/2020
:Support: mybrid@thegmu.com
:Version: 1.3.0

----

- Documentation: http://the-gmu-pypi-template.readthedocs.org/
- Source Code: https://bitbucket.org/thegmu/thegmu-pypi-template

.. image:: https://www.thegmu.com/jaz/static/img/birdie_logo_64x96.png
     

Introduction
------------

The GMU PyPi Template s a general Python project layout to create a PYPI project and is used for all PYPI Python projects at The Gregg & Mybrid Upgrade, Inc. (The GMU). The Makefile provided can immediately publish a package file to https://pypi.org, assuming you have an account. 

Feel free to clone the source code to make this your own:

::

 git clone https://bitbucket.org/thegmu/thegmu-pypi-template

----

'fun_stuff' Sample Instructions
-------------------------------

::

 # Create /tmp/fun_stuff sample project
 # 1. Create a Python3 virtualenv.
 mkdir -p /tmp/venv
 python3 -m venv /tmp/venv/py3_fun_stuff


 # 3. Activate the Python3 virtualenv.
 . /tmp/venv/py3_fun_stuff/bin/activate

 # 2. Create an empty Python3 project directory.
 mkdir -p /tmp/git/fun_stuff

 # 5. Change directory into the empty Python3 project directory.
 cd  /tmp/git/fun_stuff

 # 4. Install thegmu-pypi-template.
 # TEST: pip install --index-url https://test.pypi.org/simple/ thegmu-pypi-template
 pip install thegmu-pypi-template


 # 6. Run the install script to install the files into the current directory.
 thegmu-pypi-template

 # 7. Activate the PYPI environment from directory /tmp/fun_stuff
 . bin/activate-fun-stuff

 # 8. Validate the fun-stuff configuration by running the following make commands. 
 make init
 make test
 make dist
 make test-dist

 # 9. Repeat the above for your new project configuration your development environment.
 #     Follow the same steps above but:
 #     Replace '/tmp/venv/fun_stuff' with your Python development virtualenv root directory and project name, i.e. "$HOME/venv/py3_my_project".
 #     Replace '/tmp/git/fun_stuff' with your development source code repository root directory, i.e. "$HOME/workspace/git/my_project".
 #     Create a new activation file and update the environment variables.
 #     cp bin/activate-fun-stuff bin/activate-my-projectname
 #     replace '. bin/activate-fun-stuff' with '. bin/activate-my-projectname'

 # 10. To make Sphinx documentation.
 make backup-docs # Create backup to compare your files with.
 make destroy-docs # Delete everything under docs/
 make docs # Runs the Sphinx wizard to initialize the conf.py file and then 'make html'.
 # Open HTML index file in browser: docs/_build/html/index.html

   
----

Requirements
------------


#. Encourage Python standards are followed for packaging and source.
#. Pylint for validating PEP8 standards of code.
#. Sphinx documentation to integrate with readthedocs.org
#. Test automation in the dedicated tests directory.
#. PyPi package deployment.
#. ReadTheDocs documentation deployment.


**Tools**:

#. **autopep8**: pep8 code beautifier
#. **pylint**: coding standards
#. **pytest**: test source
#. **readthedocs.org**: public documentation using sphinx
#. **sphinx**: html documentation
#. **tox**: test the source as installed package
#. **twine**: deploy the package to pypi.org, test.pypi.org
#. **Makefile**: run the tools


**Configuration files**:

#. **.gitignore**: ignore pylint, pytest, tox and build files as well .settings, .project, and .pydevproject directories from Eclipse.
#. **.pylintrc**: The GMU specific PEP8 suppression.

----

Makefile Options
----------------

make <option>

_default:
 Same as help.

backup-docs:
 Create a temp directory, 'docs.tmp.XXX', using mktemp and copy the docs directory to it.

clean:
 Removes Python compiled files, pytest files, and tox test files. 
 See clean-pyc and clean-tox.

clean-dist:
 Removes Python packaging files.

clean-docs:
 Removes sphinx documentation build files. Configuration files are not removed. 

clean-pyc:
 Removes Python compiled files and pytest files. 

clean-tox: 
 Removes tox test files. 

destroy-docs
 Removes all sphinx config and manually edited document files as well as all generated files.
 See clean-docs.
 See backup-docs.

dist:
 Creates source and binary Python packages suitable for PyPi. 

docs:
 Build the the HTML documentation files in docs/_build.

help:
 Displays this file.

init:
 #. Install Python tools used by this Makefile.
 #. Run project-init, see project-init.

pep8:
    Run ``autopep8`` and update all the project and test files in place with white space changes.

project-init:
 #. setup.py: NAME, AUTHOR, AUTHOR_EMAIL, URL, SCRIPTS all updated.
 #. test/sample_test.py: import of project name updated.
 #. tox.ini: envlist updated

publish:
 #. Publish the package to production 'pypi.org'.
 #. User name and password prompt are given.

publish-test:
 Publish the package to test 'test-pypi.org'.
 User name and password prompt are given.

pylint:
 Run ``pylint`` and output results. No other action is taken. See ``pep8`` option to fix white space problems.

requirements:
 Python 'pip' packages for the tools.

test:
 Run the tests from source using pytest.

test-dist:
 Run the tests from virtual envinorments using tox. Builds the package and then run the test as packages in temporary Python virtualenv environments.

upgrade:
 Upgrade Python 'pip' packages for the tools. 

----

    The reasonable person adapts themself to the world; the unreasonable one persists in trying to adapt the world to themself.  Therefore all progress depends on the unreasonable person. --George Bernard Shaw

**The End**
