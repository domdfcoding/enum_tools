# stdlib
import inspect


def _is_descriptor(obj):
	"""Returns True if obj is a descriptor, False otherwise."""
	return (hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__'))


def _is_dunder(name):
	"""Returns True if a __dunder__ name, False otherwise."""
	return (name[:2] == name[-2:] == '__' and name[2:3] != '_' and name[-3:-2] != '_' and len(name) > 4)


def _is_sunder(name):
	"""Returns True if a _sunder_ name, False otherwise."""
	return (name[0] == name[-1] == '_' and name[1:2] != '_' and name[-2:-1] != '_' and len(name) > 2)


def _reduce_ex_by_name(self, proto):
	return self.name


def enumsort(things):
	"""
	sorts things by value if all same type; otherwise by name
	"""
	if not things:
		return things
	sort_type = type(things[0])
	if not issubclass(sort_type, tuple):
		# direct sort or type error
		if not all((type(v) is sort_type) for v in things[1:]):
			raise TypeError('cannot sort items of different types')
		return sorted(things)
	else:
		# expecting list of (name, value) tuples
		sort_type = type(things[0][1])
		try:
			if all((type(v[1]) is sort_type) for v in things[1:]):
				return sorted(things, key=lambda i: i[1])
			else:
				raise TypeError('try name sort instead')
		except TypeError:
			return sorted(things, key=lambda i: i[0])


def _make_class_unpicklable(cls):
	"""Make the given class un-picklable."""

	def _break_on_call_reduce(self, protocol=None):
		raise TypeError(f'{self!r} cannot be pickled')

	cls.__reduce_ex__ = _break_on_call_reduce
	cls.__module__ = '<unknown>'


def _check_auto_args(method):
	"""check if new generate method supports *args and **kwds"""
	if isinstance(method, staticmethod):
		method = method.__get__(type)
	method = getattr(method, 'im_func', method)
	args, varargs, keywords, defaults = inspect.getargspec(method)
	return varargs is not None and keywords is not None


def _get_attr_from_chain(cls, attr):
	sentinel = object()
	for basecls in cls.mro():
		obj = basecls.__dict__.get(attr, sentinel)
		if obj is not sentinel:
			return obj
