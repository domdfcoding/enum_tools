======================================================
:mod:`~enum_tools.autoenum` Sphinx Extension
======================================================

Supports most of the options used by `autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_.

Demo
----------

**These two have been created with** ``automodule``.

.. code-block:: rest

	.. automodule:: enum_tools.demo
		:members:

.. automodule:: enum_tools.demo
	:members:
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
