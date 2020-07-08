How to Install *Assign_GUP*
###########################

The basic installation procedure:

#. install Python 2.7
#. install Assign_GUP

Background
**********

This program requires Python 2.7 (not ready for Python 3 yet)
and several additional packages.  Most of the package dependencies
are met by using a Python distribution (provides Python, the basic 
package suite, and other popular packages).

The major package requirements are:

* *PyQt4* : provides the graphical user interface widgets
* *lxml* : XML support
* *pyRestTable* : presents information in a sensible table format

Python
******

Use the Anaconda Python 2.7 distribution [#]_ as it
contains most of the packages used by this program.

1. Download an installer: https://www.anaconda.com/downloads (for your OS)
2. Install on your computer.

.. [#] https://www.anaconda.com

*Assign_GUP*
************

Install *Assign_GUP* from the Python Package Index (PyPI) 
using the *pip* command after creating and activating a 
custom conda environment with the required libraries
and python version (2.7).

1. Activate [#]_ the conda *base* environment.
2. create a new conda environment::

    conda create -n assign_gup \
        python=2.7 lxml qt=4 pyqt pyRestTable \
        -c defaults \
        -c conda-forge \
        -c aps-anl-tag

3. Activate the new environment: ``conda activate assign_gup``
4. install Assign_GUP: ``pip install --no-deps Assign_GUP``

.. [#] activate: https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html


Updating *Assign_GUP*
---------------------

To update to a newer version of *Assign_GUP*, use this command::

    pip install -U --no-deps Assign_GUP

The ``-U`` option tells *pip* to search for and install the 
latest package update.

Alternative Installation steps
------------------------------

It is possible to install **Assign_GUP** using steps 
common to Python developers, such as::

     pip install https://github.com/prjemian/assign_gup

or::

    git clone install https://github.com/prjemian/assign_gup.git
    cd assign_gup
    python ./setup.py install

These are not recommended for regular use.
