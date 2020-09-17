======================================================
:mod:`~enum_tools.autoenum` Sphinx Extension
======================================================

.. rst:directive:: autoenum
.. rst:directive:: autoflag

	Used to document :class:`Enums <enum.Enum>` and :class:`Flags <enum.Flag>` respectively.

	The directives support the same options as :rst:dir:`autoclass`, but with a few changes to the behaviour:

	* Enum members are always shown regardless of whether they are documented or not.
	* Enum members are grouped separately from methods.

	The docstrings of the Enum members are taken from their ``__doc__`` attributes.
	This can be set during initialisation of the enum (see an example `here <https://stackoverflow.com/a/50473952>`_),
	with the :class:`~enum_tools.documentation.DocumentedEnum` class, or with the :func:`~enum_tools.documentation.document_enum` decorator.

	See https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html for further details.

.. rst:role:: py:enum:mem
              py:enum:member
              py:flag:mem
              py:flag:member

	Provides cross-references to Enum/Flag members.

	Unlike a standard ``:class:`` or ``:enum:`` xref the default behaviour of the
	``~`` prefix is to show both the Enum's name and the member's name, e.g.

	.. rest-example::

		:py:enum:mem:`~enum_tools.demo.StatusFlags.Running`

	The original behaviour can be restored by using the ``+`` prefix, e.g.

	.. rest-example::

		:py:enum:mem:`+enum_tools.demo.StatusFlags.Running`

-------

.. extensions:: enum_tools.autoenum


Demo
----------

**These two have been created with** ``automodule``.

.. code-block:: rest

	.. automodule:: enum_tools.demo
		:members:

.. automodule:: enum_tools.demo
	:members:
	:exclude-members: NoMemberDoc,StatusFlags
	:noindex:
	:no-autosummary:


**This one has been created with** ``autoenum``.

.. rest-example::

	.. autoenum:: enum_tools.demo.People
		:members:


**If members don't have their own docstrings no docstring is shown:**

.. rest-example::

	.. autoenum:: enum_tools.demo.NoMemberDoc
		:members:

:class:`enum.Flag`\s **can also be documented:**

.. rest-example::

	.. autoflag:: enum_tools.demo.StatusFlags
		:members:
