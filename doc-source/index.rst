===========================
enum_tools
===========================

.. start short_desc

**Alternative method for documenting enums with Sphinx.**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/enum_tools/latest?logo=read-the-docs
	:target: https://enum_tools.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

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

.. |license| image:: https://img.shields.io/github/license/domdfcoding/enum_tools
	:target: https://github.com/domdfcoding/enum_tools/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/enum_tools
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/enum_tools/v0.0.1
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

.. end shields


This package has three aims:

#. Import from the stdlib ``enum`` module when running mypy, and from ``aenum`` when the code actually runs. This helps mypy understand type annotations, but keeps all of the ``if TYPE_CHECKING:`` code in one place.

#. Provide a decorator to add docstrings to ``Enum`` members from a comment at the end of the line.

#. Provide a ``Sphinx`` extension to document ``Enum``s better that ``autoclass`` can currently.


Installation
--------------

.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			python3 -m pip install enum_tools --user


	.. tab:: from GitHub

		.. prompt:: bash

			python3 -m pip install git+https://github.com/domdfcoding/enum_tools@master --user

.. end installation

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	API Reference<docs>
	demo
	Source
	Building

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/enum_tools>`__

.. end links
