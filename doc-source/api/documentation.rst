===================================
:mod:`enum_tools.documentation`
===================================

.. module:: enum_tools.documentation
.. autosummary-widths:: 35/100

Core Functionality
--------------------

.. automodule:: enum_tools.documentation
	:noindex:
	:no-members:
	:autosummary-members: DocumentedEnum,document_enum,document_member

.. autoenum:: enum_tools.documentation.DocumentedEnum

.. autodecorator:: enum_tools.documentation.document_enum

.. autofunction:: enum_tools.documentation.document_member


.. latex:clearpage::


Warnings
--------------------

.. autoexception:: enum_tools.documentation.MultipleDocstringsWarning
	:exclude-members: __str__

Utilities
--------------------

.. deprecated:: v0.9.0  These utilities will be removed in v1.0.0.

.. automodulesumm:: enum_tools.documentation
	:autosummary-exclude-members: DocumentedEnum,document_enum,document_member,MultipleDocstringsWarning

.. autofunction:: enum_tools.documentation.get_base_indent

.. autofunction:: enum_tools.documentation.get_dedented_line

.. autofunction:: enum_tools.documentation.get_tokens

.. autofunction:: enum_tools.documentation.parse_tokens
