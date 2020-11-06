============
Enum Tools
============

.. start short_desc

**Tools to expand Python's enum module.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/enum_tools/latest?logo=read-the-docs
	:target: https://enum_tools.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/enum_tools/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/enum_tools/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/enum_tools
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/enum_tools/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/enum_tools/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/enum_tools/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/enum_tools/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/enum_tools/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/enum_tools?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/enum_tools?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/enum_tools
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/enum_tools?logo=python&logoColor=white
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/enum_tools?logo=anaconda
	:target: https://anaconda.org/domdfcoding/enum_tools
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/enum_tools?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/enum_tools
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/enum_tools
	:target: https://github.com/domdfcoding/enum_tools/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/enum_tools
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/enum_tools/v0.6.1
	:target: https://github.com/domdfcoding/enum_tools/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/enum_tools
	:target: https://github.com/domdfcoding/enum_tools/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/enum_tools/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/enum_tools/master
	:alt: pre-commit.ci status

.. end shields

|

This package has two features:

#. A decorator to add docstrings to ``Enum`` members from a comment at the end of the line.

#. A ``Sphinx`` extension to document Enums better than ``autoclass`` can currently.


Installation
--------------

.. start installation

``enum_tools`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install enum_tools

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/domdfcoding
		$ conda config --add channels http://conda.anaconda.org/conda-forge

	* Then install

	.. code-block:: bash

		$ conda install enum_tools

.. end installation


Further Reading
-----------------------

#. https://docs.python.org/3/library/enum.html

#. `Is it possible to define a class constant inside an Enum? <https://stackoverflow.com/q/17911188/3092681>`_

#. `Enums with Attributes <https://stackoverflow.com/a/19300424/3092681>`_

#. `When should I subclass EnumMeta instead of Enum? <https://stackoverflow.com/a/43730306/3092681>`_
