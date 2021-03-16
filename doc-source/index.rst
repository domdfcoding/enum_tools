============
Enum Tools
============

.. start short_desc

**Tools to expand Python's enum module.**

.. end short_desc


.. .. code-block:: python

.. 	class Tools(Enum):
		Hammer = "🔨"
		Spanner = "🔧"
		Scissors = "✂️"


.. start shields

.. only:: html

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
		  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: enum_tools
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| requires-io-shield::
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: enum_tools
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: enum_tools
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: enum_tools
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: enum_tools
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/enum_tools?logo=anaconda
		:target: https://anaconda.org/domdfcoding/enum_tools
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/enum_tools?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/enum_tools
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.6.4
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2021
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: enum_tools
		:downloads: month
		:alt: PyPI - Downloads

	.. |pre_commit_ci| pre-commit-ci-shield::
		:alt: pre-commit.ci status

.. end shields


This library provides the following:

#. A decorator to add docstrings to ``Enum`` members from a comment at the end of the line.

#. A ``Sphinx`` extension to document Enums better than :rst:dir:`autoclass` can currently.

#. Additional ``Enum`` classes with different functionality.


Installation
--------------

.. start installation

.. installation:: enum_tools
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	autoenum

.. toctree::
	:maxdepth: 3
	:caption: API Reference
	:glob:

	api/*

.. toctree::
	:maxdepth: 3
	:caption: Contributing

	contributing
	Source

.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	`Browse the GitHub Repository <https://github.com/domdfcoding/enum_tools>`__

.. end links


Further Reading
-----------------------

#. https://docs.python.org/3/library/enum.html

#. `Is it possible to define a class constant inside an Enum? <https://stackoverflow.com/q/17911188/3092681>`_

#. `Enums with Attributes <https://stackoverflow.com/a/19300424/3092681>`_

#. `When should I subclass EnumMeta instead of Enum? <https://stackoverflow.com/a/43730306/3092681>`_
