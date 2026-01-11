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
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/enum-tools/latest?logo=read-the-docs
	:target: https://enum-tools.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/enum_tools/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/enum_tools/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/enum_tools/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/enum_tools/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/enum_tools/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/enum_tools/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/enum_tools/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/enum_tools/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/enum_tools/
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

.. |conda-version| image:: https://img.shields.io/conda/v/conda-forge/enum_tools?logo=anaconda
	:target: https://anaconda.org/conda-forge/enum_tools
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/conda-forge/enum_tools?label=conda%7Cplatform
	:target: https://anaconda.org/conda-forge/enum_tools
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/enum_tools
	:target: https://github.com/domdfcoding/enum_tools/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/enum_tools
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/enum_tools/v0.13.0
	:target: https://github.com/domdfcoding/enum_tools/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/enum_tools
	:target: https://github.com/domdfcoding/enum_tools/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2026
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/enum_tools
	:target: https://pypistats.org/packages/enum_tools
	:alt: PyPI - Downloads

.. end shields


This library provides the following:

#. ``enum_tools.autoenum`` – A `Sphinx <https://www.sphinx-doc.org>`_ extension to document Enums better than ``autoclass``
   can currently.
#. ``@enum_tools.documentation.document_enum`` – A decorator to add docstrings to ``Enum`` members
   from a comment at the end of the line.
#. ``enum_tools.custom_enums`` – Additional ``Enum`` classes with different functionality.


Installation
--------------

.. start installation

``enum_tools`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install enum_tools

To install with ``conda``:

.. code-block:: bash

	$ conda install -c conda-forge enum_tools

.. end installation


Further Reading
-----------------------

#. https://docs.python.org/3/library/enum.html

#. `Is it possible to define a class constant inside an Enum? <https://stackoverflow.com/q/17911188/3092681>`_

#. `Enums with Attributes <https://stackoverflow.com/a/19300424/3092681>`_

#. `When should I subclass EnumMeta instead of Enum? <https://stackoverflow.com/a/43730306/3092681>`_
