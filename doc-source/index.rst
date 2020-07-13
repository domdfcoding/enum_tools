===========================
enum_tools
===========================

.. start short_desc

**Fork of the Advanced Enumeration library with better support for mypy, docstrings and Sphinx.**

.. end short_desc

.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs|
	* - Tests
	  - |travis| |requires| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Other
	  - |license| |language| |commits-since| |commits-latest| |maintained| 

.. |docs| image:: https://img.shields.io/readthedocs/enum_tools/latest?logo=read-the-docs
	:target: https://enum_tools.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/enum_tools/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/enum_tools
	:alt: Travis Build Status

.. |requires| image:: https://requires.io/github/domdfcoding/enum_tools/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/enum_tools/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://shields.io/coveralls/github/domdfcoding/enum_tools/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/enum_tools?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/enum_tools?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/enum_tools
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/enum_tools
	:target: https://pypi.org/project/enum_tools/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/enum_tools
	:alt: License
	:target: https://github.com/domdfcoding/enum_tools/blob/master/LICENSE

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

			pip install enum_tools


	.. tab:: from GitHub

		.. prompt:: bash

			pip install git+https://github.com//enum_tools@master

.. end installation

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	API Reference<docs>
	Source
	Building

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/enum_tools>`__

.. end links
