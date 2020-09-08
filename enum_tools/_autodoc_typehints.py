# Temporary vendoring of sphinx_autodoc_typehints until changes merged upstream.
#
# This is the MIT license: http://www.opensource.org/licenses/mit-license.php
#
# Copyright (c) Alex Grönholm
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

# stdlib
import inspect
from typing import AnyStr, TypeVar

# 3rd party
import sphinx_autodoc_typehints  # type: ignore
from sphinx.util.inspect import signature as Signature
from sphinx.util.inspect import stringify_signature

__all__ = ["format_annotation", "process_signature"]


def format_annotation(annotation, fully_qualified: bool = False) -> str:
	# Special cases
	if annotation is None or annotation is type(None):  # noqa: E721
		return ':py:obj:`None`'
	elif annotation is Ellipsis:
		return '...'

	# Type variables are also handled specially
	try:
		if isinstance(annotation, TypeVar) and annotation is not AnyStr:  # type: ignore
			return f':py:data:`\\{annotation!r}`'
	except TypeError:
		pass

	try:
		module = sphinx_autodoc_typehints.get_annotation_module(annotation)
		class_name = sphinx_autodoc_typehints.get_annotation_class_name(annotation, module)
		args = sphinx_autodoc_typehints.get_annotation_args(annotation, module, class_name)
	except ValueError:
		return str(annotation)

	# Redirect all typing_extensions types to the stdlib typing module
	if module == 'typing_extensions':
		module = 'typing'

	full_name = (module + '.' + class_name) if module != 'builtins' else class_name
	prefix = '' if fully_qualified or full_name == class_name else '~'
	role = 'data' if class_name in sphinx_autodoc_typehints.pydata_annotations else 'class'
	args_format = '\\[{}]'
	formatted_args = ''

	# Some types require special handling
	if full_name == 'typing.NewType':
		args_format = f'\\(:py:data:`~{annotation.__name__}`, {{}})'
		role = 'func'
	elif full_name == 'typing.Union' and len(args) == 2 and type(None) in args:
		full_name = 'typing.Optional'
		args = tuple(x for x in args if x is not type(None))  # noqa: E721
	elif full_name == 'typing.Callable' and args and args[0] is not ...:
		formatted_args = '\\[\\[' + ', '.join(format_annotation(arg) for arg in args[:-1]) + ']'
		formatted_args += ', ' + format_annotation(args[-1]) + ']'
	elif full_name == 'typing.Literal':
		formatted_args = '\\[' + ', '.join(repr(arg) for arg in args) + ']'

	if args and not formatted_args:
		formatted_args = args_format.format(', '.join(format_annotation(arg, fully_qualified) for arg in args))

	return ':py:{role}:`{prefix}{full_name}`{formatted_args}'.format(
			role=role, prefix=prefix, full_name=full_name, formatted_args=formatted_args
			)


def process_signature(app, what: str, name: str, obj, options, signature, return_annotation):
	if not callable(obj):
		return

	original_obj = obj
	if inspect.isclass(obj):
		obj = getattr(obj, '__init__', getattr(obj, '__new__', None))

	if not getattr(obj, '__annotations__', None):
		return

	obj = inspect.unwrap(obj)

	try:
		signature = Signature(obj)
	except ValueError:
		return signature, return_annotation

	parameters = [param.replace(annotation=inspect.Parameter.empty) for param in signature.parameters.values()]

	# The generated dataclass __init__() is weird and needs the second condition
	if '<locals>' in obj.__qualname__ and not (what == 'method' and name.endswith('.__init__')):
		sphinx_autodoc_typehints.logger.warning(
				'Cannot treat a function defined as a local function: "%s"  (use @functools.wraps)', name
				)
		return

	if parameters:
		if inspect.isclass(original_obj) or (what == 'method' and name.endswith('.__init__')):
			del parameters[0]
		elif what == 'method':
			outer = inspect.getmodule(obj)
			for clsname in obj.__qualname__.split('.')[:-1]:
				outer = getattr(outer, clsname)

			method_name = obj.__name__
			if method_name.startswith("__") and not method_name.endswith("__"):
				# If the method starts with double underscore (dunder)
				# Python applies mangling so we need to prepend the class name.
				# This doesn't happen if it always ends with double underscore.
				class_name = obj.__qualname__.split('.')[-2]
				method_name = f"_{class_name}{method_name}"

			method_object = outer.__dict__[method_name] if outer else obj
			if not isinstance(method_object, (classmethod, staticmethod)):
				del parameters[0]

	signature = signature.replace(parameters=parameters, return_annotation=inspect.Signature.empty)

	return stringify_signature(signature).replace('\\', '\\\\'), None


sphinx_autodoc_typehints.format_annotation = format_annotation
sphinx_autodoc_typehints.process_signature = process_signature
