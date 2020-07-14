# Based on https://github.com/pauleveritt/customizing_sphinx/tree/master/tests/integration
# and https://github.com/sphinx-doc/sphinx/issues/7008

# stdlib
from decimal import Decimal
from enum import Enum
from pathlib import Path

# 3rd party
import pytest

# this package
from enum_tools.autoenum import EnumDocumenter


@pytest.mark.parametrize("obj", [
		"abcdefg",
		b"abcdefg",
		b"\x00\x01",
		12345,
		123.45,
		Decimal(123.45),
		Path("."),
		])
def test_cannot_document_member(obj):
	assert not EnumDocumenter.can_document_member(obj, '', True, '')


class MyEnum(Enum):
	foo = 1
	bar = 2


def test_can_document_member():
	assert EnumDocumenter.can_document_member(MyEnum, '', True, '')


def test(app):
	# app is a Sphinx application object for default sphinx project (`tests/roots/test-root`).
	app.build()


# @pytest.mark.sphinx(buildername='latex')
# def test_latex(app):
# 	# latex builder is chosen here.
# 	app.build()

# pytestmark = pytest.mark.sphinx('html', testroot='root')


@pytest.mark.parametrize(
		'page', [
				'index.html',
				], indirect=True
		)
def test_index(page):
	# Make sure the page title is what you expect
	title = page.find('h1').contents[0].strip()
	assert 'autoenum Demo' == title

	# Now test the directive

	class_count = 0

	for class_ in page.findAll("dl"):
		if "class" not in class_["class"]:
			continue

		if class_count == 0:
			assert class_.find("dt")["id"] == "enum_tools.demo.People"
		elif class_count == 1:
			assert class_.find("dt")["id"] == "id0"
		assert class_.find("dd").findAll("p")[0].contents[0] == "An enumeration of people"
		assert class_.find("dd").findAll("p")[1].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.findAll("dl"):
			if "attribute" not in attr["class"]:
				continue

			if attr_count == 0:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.People.Bob"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id1"
				assert attr.find("dt").em.contents[0] == " = <People.Bob: 1>"
				assert str(attr.find("dd").contents[0]) == "<p>A person called Bob</p>"
			elif attr_count == 1:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.People.Alice"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id2"
				assert attr.find("dt").em.contents[0] == " = <People.Alice: 2>"
				assert str(attr.find("dd").contents[0]) == "<p>A person called Alice</p>"
			elif attr_count == 2:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.People.Carol"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id3"
				assert attr.find("dt").em.contents[0] == " = <People.Carol: 3>"
				assert str(attr.find("dd").contents[0]) == "<p>A person called Carol</p>"

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2
