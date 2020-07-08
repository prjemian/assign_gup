
==================
README: Assign_GUP
==================

**Assist in assigning APS GUPs to PRP members**

:author: 	Pete R. Jemian
:email:  	jemian@anl.gov
:copyright: 2005-2017, UChicago Argonne, LLC
:license:   ANL OPEN SOURCE LICENSE (see *LICENSE*)
:docs:      http://assign_gup.readthedocs.io
:git:       https://github.com/prjemian/assign_gup.git
:PyPI:      https://pypi.python.org/pypi/assign_gup
:TODO list: https://github.com/prjemian/assign_gup/issues

.. * **build badges**:
   .. image:: https://travis-ci.org/prjemian/assign_gup.svg?branch=master
      :target: https://travis-ci.org/prjemian/assign_gup
   .. image:: https://coveralls.io/repos/github/prjemian/assign_gup/badge.svg?branch=master
      :target: https://coveralls.io/github/prjemian/assign_gup?branch=master

* **release badges**:
   .. image:: https://img.shields.io/github/tag/prjemian/assign_gup.svg
      :target: https://github.com/prjemian/assign_gup/tags
   .. image:: https://img.shields.io/github/release/prjemian/assign_gup.svg
      :target: https://github.com/prjemian/assign_gup/releases
   .. image:: https://img.shields.io/pypi/v/assign_gup.svg
      :target: https://pypi.python.org/pypi/assign_gup/
   .. image:: https://anaconda.org/prjemian/assign_gup/badges/version.svg
      :target: https://anaconda.org/prjemian/assign_gup


* **community badges**
   .. image:: http://depsy.org/api/package/pypi/assign_gup/badge.svg
      :target: http://depsy.org/package/python/assign_gup
   .. image:: https://badges.gitter.im/assign_gup/Lobby.svg
      :alt: Join the chat at https://gitter.im/assign_gup/Lobby
      :target: https://gitter.im/assign_gup/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

Install and Run
---------------

1. Install Anaconda Python (https://anaconda.com/downloads)
2. Activate the *conda* ``base`` environment. (advice: https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
3. Create a custom conda environment::

      conda create -n assign_gup \
         python=2 lxml qt=4 pyqt pyRestTable \
         -c defaults \
         -c conda-forge \
         -c aps-anl-tag

4. Activate the new environment: ``conda activate assign_gup``
5. Install: ``pip install --no-deps Assign_GUP``
6. Run: ``Assign_GUP``
