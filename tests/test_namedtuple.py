# -*- coding: utf-8 -*-

# stdlib
from unittest import TestCase

# 3rd party
from aenum import TupleSize # type: ignore

# this package
from better_enum import NamedTuple
from tests.demo_classes import DeathForm, LifeForm, ThatsIt


class TestNamedTuple(TestCase):

	def test_explicit_indexing(self):

		class Person(NamedTuple):
			age = 0
			first = 1
			last = 2

		p1 = Person(17, 'John', 'Doe')
		p2 = Person(21, 'Jane', 'Doe')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p2[0], 21)
		self.assertEqual(p2[1], 'Jane')
		self.assertEqual(p2[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')
		self.assertEqual(p2.age, 21)
		self.assertEqual(p2.first, 'Jane')
		self.assertEqual(p2.last, 'Doe')

	def test_implicit_indexing(self):

		class Person(NamedTuple):
			__order__ = "age first last"
			age = "person's age"
			first = "person's first name"
			last = "person's last name"

		p1 = Person(17, 'John', 'Doe')
		p2 = Person(21, 'Jane', 'Doe')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p2[0], 21)
		self.assertEqual(p2[1], 'Jane')
		self.assertEqual(p2[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')
		self.assertEqual(p2.age, 21)
		self.assertEqual(p2.first, 'Jane')
		self.assertEqual(p2.last, 'Doe')

	def test_mixed_indexing(self):

		class Person(NamedTuple):
			__order__ = "age last cars"
			age = "person's age"
			last = 2, "person's last name"
			cars = "person's cars"

		p1 = Person(17, 'John', 'Doe', 3)
		p2 = Person(21, 'Jane', 'Doe', 9)
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p1[3], 3)
		self.assertEqual(p2[0], 21)
		self.assertEqual(p2[1], 'Jane')
		self.assertEqual(p2[2], 'Doe')
		self.assertEqual(p2[3], 9)
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.last, 'Doe')
		self.assertEqual(p1.cars, 3)
		self.assertEqual(p2.age, 21)
		self.assertEqual(p2.last, 'Doe')
		self.assertEqual(p2.cars, 9)

	def test_issubclass(self):

		class Person(NamedTuple):
			age = 0
			first = 1
			last = 2

		self.assertTrue(issubclass(Person, NamedTuple))
		self.assertTrue(issubclass(Person, tuple))

	def test_isinstance(self):

		class Person(NamedTuple):
			age = 0
			first = 1
			last = 2

		p1 = Person(17, 'John', 'Doe')
		self.assertTrue(isinstance(p1, Person))
		self.assertTrue(isinstance(p1, NamedTuple))
		self.assertTrue(isinstance(p1, tuple))

	def test_explicit_indexing_after_functional_api(self):
		Person = NamedTuple('Person', (('age', 0), ('first', 1), ('last', 2)))
		p1 = Person(17, 'John', 'Doe')
		p2 = Person(21, 'Jane', 'Doe')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p2[0], 21)
		self.assertEqual(p2[1], 'Jane')
		self.assertEqual(p2[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')
		self.assertEqual(p2.age, 21)
		self.assertEqual(p2.first, 'Jane')
		self.assertEqual(p2.last, 'Doe')

	def test_implicit_indexing_after_functional_api(self):
		Person = NamedTuple('Person', 'age first last')
		p1 = Person(17, 'John', 'Doe')
		p2 = Person(21, 'Jane', 'Doe')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p2[0], 21)
		self.assertEqual(p2[1], 'Jane')
		self.assertEqual(p2[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')
		self.assertEqual(p2.age, 21)
		self.assertEqual(p2.first, 'Jane')
		self.assertEqual(p2.last, 'Doe')

	def test_mixed_indexing_after_functional_api(self):
		Person = NamedTuple('Person', (('age', 0), ('last', 2), ('cars', 3)))
		p1 = Person(17, 'John', 'Doe', 3)
		p2 = Person(21, 'Jane', 'Doe', 9)
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p1[3], 3)
		self.assertEqual(p2[0], 21)
		self.assertEqual(p2[1], 'Jane')
		self.assertEqual(p2[2], 'Doe')
		self.assertEqual(p2[3], 9)
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.last, 'Doe')
		self.assertEqual(p1.cars, 3)
		self.assertEqual(p2.age, 21)
		self.assertEqual(p2.last, 'Doe')
		self.assertEqual(p2.cars, 9)

	def test_issubclass_after_functional_api(self):
		Person = NamedTuple('Person', 'age first last')
		self.assertTrue(issubclass(Person, NamedTuple))
		self.assertTrue(issubclass(Person, tuple))

	def test_isinstance_after_functional_api(self):
		Person = NamedTuple('Person', 'age first last')
		p1 = Person(17, 'John', 'Doe')
		self.assertTrue(isinstance(p1, Person))
		self.assertTrue(isinstance(p1, NamedTuple))
		self.assertTrue(isinstance(p1, tuple))

	def test_creation_with_all_keywords(self):
		Person = NamedTuple('Person', 'age first last')
		p1 = Person(age=17, first='John', last='Doe')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')

	def test_creation_with_some_keywords(self):
		Person = NamedTuple('Person', 'age first last')
		p1 = Person(17, first='John', last='Doe')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')
		p1 = Person(17, last='Doe', first='John')
		self.assertEqual(p1[0], 17)
		self.assertEqual(p1[1], 'John')
		self.assertEqual(p1[2], 'Doe')
		self.assertEqual(p1.age, 17)
		self.assertEqual(p1.first, 'John')
		self.assertEqual(p1.last, 'Doe')
	#
	# def test_custom_new(self):
	#
	# 	class Book(NamedTuple):
	# 		title = 0
	# 		author = 1
	# 		genre = 2
	#
	# 		def __new__(cls, string):
	# 			args = [s.strip() for s in string.split(';')]
	# 			return super(Book, cls).__new__(cls, *tuple(args))
	#
	# 	b1 = Book('The Last Mohican; John Doe; Historical')
	# 	self.assertEqual(b1.title, 'The Last Mohican')
	# 	self.assertEqual(b1.author, 'John Doe')
	# 	self.assertEqual(b1.genre, 'Historical')

	def test_defaults_in_class(self):

		class Character(NamedTuple):
			name = 0
			gender = 1, None, 'male'
			klass = 2, None, 'fighter'

		for char in (
				{'name': 'John Doe'},
				{'name': 'William Pickney', 'klass': 'scholar'},
				{'name': 'Sarah Doughtery', 'gender': 'female'},
				{'name': 'Sissy Moonbeam', 'gender': 'female', 'klass': 'sorceress'},
				):
			c = Character(**char)
			for name, value in (('name', None), ('gender', 'male'), ('klass', 'fighter')):
				if name in char:
					value = char[name]
				self.assertEqual(getattr(c, name), value)

	# def test_defaults_in_class_that_are_falsey(self):
	#
	# 	class Point(NamedTuple):
	# 		x = 0, 'horizondal coordinate', 0
	# 		y = 1, 'vertical coordinate', 0
	#
	# 	p = Point()
	# 	self.assertEqual(p.x, 0)
	# 	self.assertEqual(p.y, 0)

	def test_pickle_namedtuple_with_module(self):
		if isinstance(LifeForm, Exception):
			raise LifeForm
		lf = LifeForm('this', 'that', 'theother')

	def test_pickle_namedtuple_without_module(self):
		if isinstance(DeathForm, Exception):
			raise DeathForm
		df = DeathForm('sickly green', '2x4', 'foul')

	def test_subclassing(self):
		if isinstance(ThatsIt, Exception):
			raise ThatsIt
		ti = ThatsIt('Henry', 'Weinhardt')
		self.assertEqual(ti.blah, 'Henry')
		self.assertTrue(ti.what(), 'Henry')

	def test_contains(self):
		Book = NamedTuple('Book', 'title author genre')
		b = Book('Teckla', 'Steven Brust', 'fantasy')
		self.assertTrue('Teckla' in b)
		self.assertTrue('Steven Brust' in b)
		self.assertTrue('fantasy' in b)
	#
	# def test_fixed_size(self):
	#
	# 	class Book(NamedTuple):
	# 		_size_ = TupleSize.fixed
	# 		title = 0
	# 		author = 1
	# 		genre = 2
	#
	# 	b = Book('Teckla', 'Steven Brust', 'fantasy')
	# 	self.assertTrue('Teckla' in b)
	# 	self.assertTrue('Steven Brust' in b)
	# 	self.assertTrue('fantasy' in b)
	# 	self.assertEqual(b.title, 'Teckla')
	# 	self.assertEqual(b.author, 'Steven Brust')
	# 	self.assertRaises(TypeError, Book, 'Teckla', 'Steven Brust')
	# 	self.assertRaises(TypeError, Book, 'Teckla')

	# def test_combining_namedtuples(self):
	#
	# 	class Point(NamedTuple):
	# 		x = 0, 'horizontal coordinate', 1
	# 		y = 1, 'vertical coordinate', -1
	#
	# 	class Color(NamedTuple):
	# 		r = 0, 'red component', 11
	# 		g = 1, 'green component', 29
	# 		b = 2, 'blue component', 37
	#
	# 	Pixel1 = NamedTuple('Pixel', Point + Color, module=__name__)
	#
	# 	class Pixel2(Point, Color):
	# 		"a colored dot"
	#
	# 	class Pixel3(Point):
	# 		r = 2, 'red component', 11
	# 		g = 3, 'green component', 29
	# 		b = 4, 'blue component', 37
	#
	# 	self.assertEqual(Pixel1._fields_, 'x y r g b'.split())
	# 	self.assertEqual(Pixel1.x.__doc__, 'horizontal coordinate')
	# 	self.assertEqual(Pixel1.x.default, 1)
	# 	self.assertEqual(Pixel1.y.__doc__, 'vertical coordinate')
	# 	self.assertEqual(Pixel1.y.default, -1)
	# 	self.assertEqual(Pixel1.r.__doc__, 'red component')
	# 	self.assertEqual(Pixel1.r.default, 11)
	# 	self.assertEqual(Pixel1.g.__doc__, 'green component')
	# 	self.assertEqual(Pixel1.g.default, 29)
	# 	self.assertEqual(Pixel1.b.__doc__, 'blue component')
	# 	self.assertEqual(Pixel1.b.default, 37)
	# 	self.assertEqual(Pixel2._fields_, 'x y r g b'.split())
	# 	self.assertEqual(Pixel2.x.__doc__, 'horizontal coordinate')
	# 	self.assertEqual(Pixel2.x.default, 1)
	# 	self.assertEqual(Pixel2.y.__doc__, 'vertical coordinate')
	# 	self.assertEqual(Pixel2.y.default, -1)
	# 	self.assertEqual(Pixel2.r.__doc__, 'red component')
	# 	self.assertEqual(Pixel2.r.default, 11)
	# 	self.assertEqual(Pixel2.g.__doc__, 'green component')
	# 	self.assertEqual(Pixel2.g.default, 29)
	# 	self.assertEqual(Pixel2.b.__doc__, 'blue component')
	# 	self.assertEqual(Pixel2.b.default, 37)
	# 	self.assertEqual(Pixel3._fields_, 'x y r g b'.split())
	# 	self.assertEqual(Pixel3.x.__doc__, 'horizontal coordinate')
	# 	self.assertEqual(Pixel3.x.default, 1)
	# 	self.assertEqual(Pixel3.y.__doc__, 'vertical coordinate')
	# 	self.assertEqual(Pixel3.y.default, -1)
	# 	self.assertEqual(Pixel3.r.__doc__, 'red component')
	# 	self.assertEqual(Pixel3.r.default, 11)
	# 	self.assertEqual(Pixel3.g.__doc__, 'green component')
	# 	self.assertEqual(Pixel3.g.default, 29)
	# 	self.assertEqual(Pixel3.b.__doc__, 'blue component')
	# 	self.assertEqual(Pixel3.b.default, 37)

	def test_function_api_type(self):

		class Tester(NamedTuple):

			def howdy(self):
				return 'backwards', list(reversed(self))

		Testee = NamedTuple('Testee', 'a c e', type=Tester)
		t = Testee(1, 2, 3)
		self.assertEqual(t.howdy(), ('backwards', [3, 2, 1]))

	# def test_asdict(self):
	#
	# 	class Point(NamedTuple):
	# 		x = 0, 'horizontal coordinate', 1
	# 		y = 1, 'vertical coordinate', -1
	#
	# 	class Color(NamedTuple):
	# 		r = 0, 'red component', 11
	# 		g = 1, 'green component', 29
	# 		b = 2, 'blue component', 37
	#
	# 	Pixel = NamedTuple('Pixel', Point + Color, module=__name__)
	# 	pixel = Pixel(99, -101, 255, 128, 0)
	# 	self.assertEqual(pixel._asdict(), {'x': 99, 'y': -101, 'r': 255, 'g': 128, 'b': 0})

	# def test_make(self):
	#
	# 	class Point(NamedTuple):
	# 		x = 0, 'horizontal coordinate', 1
	# 		y = 1, 'vertical coordinate', -1
	#
	# 	self.assertEqual(Point(4, 5), (4, 5))
	# 	self.assertEqual(Point._make((4, 5)), (4, 5))

	def test_replace(self):

		class Color(NamedTuple):
			r = 0, 'red component', 11
			g = 1, 'green component', 29
			b = 2, 'blue component', 37

		purple = Color(127, 0, 127)
		mid_gray = purple._replace(g=127)
		self.assertEqual(mid_gray, (127, 127, 127))

	# def test_fixed_size(self):
	#
	# 	class Book(NamedTuple, size=TupleSize.fixed):
	# 		title = 0
	# 		author = 1
	# 		genre = 2
	#
	# 	b = Book('Teckla', 'Steven Brust', 'fantasy')
	# 	self.assertTrue('Teckla' in b)
	# 	self.assertTrue('Steven Brust' in b)
	# 	self.assertTrue('fantasy' in b)
	# 	self.assertEqual(b.title, 'Teckla')
	# 	self.assertEqual(b.author, 'Steven Brust')
	# 	self.assertRaises(TypeError, Book, 'Teckla', 'Steven Brust')
	# 	self.assertRaises(TypeError, Book, 'Teckla')

	def test_minimum_size(self):

		class Book(NamedTuple):
			_size_ = TupleSize.minimum
			title = 0
			author = 1

		b = Book('Teckla', 'Steven Brust', 'fantasy')
		self.assertTrue('Teckla' in b)
		self.assertTrue('Steven Brust' in b)
		self.assertTrue('fantasy' in b)
		self.assertEqual(b.title, 'Teckla')
		self.assertEqual(b.author, 'Steven Brust')
		b = Book('Teckla', 'Steven Brust')
		self.assertTrue('Teckla' in b)
		self.assertTrue('Steven Brust' in b)
		self.assertEqual(b.title, 'Teckla')
		self.assertEqual(b.author, 'Steven Brust')
		self.assertRaises(TypeError, Book, 'Teckla')

	def test_variable_size(self):

		class Book(NamedTuple):
			_size_ = TupleSize.variable
			title = 0
			author = 1
			genre = 2

		b = Book('Teckla', 'Steven Brust', 'fantasy')
		self.assertTrue('Teckla' in b)
		self.assertTrue('Steven Brust' in b)
		self.assertTrue('fantasy' in b)
		self.assertEqual(b.title, 'Teckla')
		self.assertEqual(b.author, 'Steven Brust')
		self.assertEqual(b.genre, 'fantasy')
		b = Book('Teckla', 'Steven Brust')
		self.assertTrue('Teckla' in b)
		self.assertTrue('Steven Brust' in b)
		self.assertEqual(b.title, 'Teckla')
		self.assertEqual(b.author, 'Steven Brust')
		self.assertRaises(AttributeError, getattr, b, 'genre')
		self.assertRaises(TypeError, Book, title='Teckla', genre='fantasy')
		self.assertRaises(TypeError, Book, author='Steven Brust')
