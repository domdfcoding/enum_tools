================================================
:mod:`enum_tools.autoenum` -- Sphinx Extension
================================================

A Sphinx directive for documenting :class:`Enums <enum.Enum>` in Python.

Provides the :rst:dir:`autoenum` directive for documenting :class:`Enums <enum.Enum>`,
and :rst:dir:`autoflag` for documenting :class:`Flags <enum.Flag>`.
These behaves much like :rst:dir:`autoclass` and :rst:dir:`autofunction`.

.. extras-require:: sphinx
	:pyproject:
	:scope: extension / module

.. extensions:: enum_tools.autoenum

.. contents:: Sections
	:depth: 1
	:local:
	:backlinks: none


Usage
---------

.. rst:directive:: autoenum
				   autoflag

	These directives are used for documenting :class:`Enums <enum.Enum>` and :class:`Flags <enum.Flag>` respectively.

	They support the same options as :rst:dir:`autoclass`, but with a few changes to the behaviour:

	* Enum members are always shown regardless of whether they are documented or not.
	* Enum members are grouped separately from methods.

	The docstrings of the Enum members are taken from their ``__doc__`` attributes.
	This can be set during initialisation of the enum (see an example `here <https://stackoverflow.com/a/50473952>`_),
	with the :class:`~enum_tools.documentation.DocumentedEnum` class, or with the :func:`~enum_tools.documentation.document_enum` decorator.

	See the `autodoc module documentation`_ for further details
	of the general :rst:dir:`autoclass` behaviour.

	.. _autodoc module documentation: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html


.. rst:role:: py:enum:mem
              py:enum:member
              py:flag:mem
              py:flag:member

	These roles provide cross-references to Enum/Flag members.

	.. versionadded:: 0.4.0

	Unlike a standard ``:class:`` or ``:enum:`` xref the default behaviour of the
	``~`` prefix is to show both the Enum's name and the member's name.
	For example:

	.. rest-example::

		:py:enum:mem:`~enum_tools.demo.StatusFlags.Running`

	The original behaviour can be restored by using the ``+`` prefix:

	.. rest-example::

		:py:enum:mem:`+enum_tools.demo.StatusFlags.Running`


.. latex:vspace:: 10px

Demo
----------

**These two have been created with** ``automodule``.

.. container:: rest-example

	.. code-block:: rest

		.. automodule:: enum_tools.demo
			:members:

	.. automodule:: enum_tools.demo
		:members:
		:exclude-members: NoMemberDoc,StatusFlags,People
		:noindex:
		:no-autosummary:

	.. latex:clearpage::

	.. automodule:: enum_tools.demo
		:members:
		:exclude-members: NoMemberDoc,StatusFlags,NoMethods
		:noindex:
		:no-autosummary:

.. raw:: html

	<p></p>


.. latex:vspace:: 10px

**This one has been created with** ``autoenum``.

.. rest-example::

	.. autoenum:: enum_tools.demo.People
		:members:


.. latex:clearpage::

**If members don't have their own docstrings no docstring is shown:**

.. rest-example::

	.. autoenum:: enum_tools.demo.NoMemberDoc
		:members:


.. latex:vspace:: 10px

**Flags can also be documented:**

.. rest-example::

	.. autoflag:: enum_tools.demo.StatusFlags
		:members:


API Reference
---------------

.. automodule:: enum_tools.autoenum
	:no-docstring:
	:exclude-members: innernodeclass
