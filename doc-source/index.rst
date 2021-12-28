============
Enum Tools
============

.. start short_desc

.. documentation-summary::
	:meta:

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
		  - |codefactor| |actions_flake8| |actions_mypy|
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

	.. |requires| image:: https://dependency-dash.herokuapp.com/github/domdfcoding/enum_tools/badge.svg
		:target: https://dependency-dash.herokuapp.com/github/domdfcoding/enum_tools/
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
		:commits-since: v0.7.0
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

.. end shields


Overview
------------

.. latex-section::


This library provides the following:

#. :mod:`enum_tools.autoenum` -- A `Sphinx <https://www.sphinx-doc.org>`_ extension to document Enums better than :rst:dir:`autoclass`
   can currently.
#. :deco:`enum_tools.documentation.document_enum` -- A decorator to add docstrings to :class:`~enum.Enum` members
   from a comment at the end of the line.
#. :mod:`enum_tools.custom_enums` -- Additional :class:`~enum.Enum` classes with different functionality.


Installation
--------------

.. start installation

.. installation:: enum_tools
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation


Contents
------------

.. html-section::


.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:glob:

	api/*


.. only:: html

	.. toctree::
		:maxdepth: 3
		:glob:

		contributing
		Source
		license

.. sidebar-links::
	:caption: Links
	:github:
	:pypi: enum_tools


.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <domdfcoding/enum_tools>`



Further Reading
-----------------------

.. html-section::


.. only:: html

	* https://docs.python.org/3/library/enum.html
	* `Is it possible to define a class constant inside an Enum? <https://stackoverflow.com/q/17911188/3092681>`_
	* `Enums with Attributes <https://stackoverflow.com/a/19300424/3092681>`_
	* `When should I subclass EnumMeta instead of Enum? <https://stackoverflow.com/a/43730306/3092681>`_
