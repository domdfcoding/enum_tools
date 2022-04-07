# Based on https://github.com/pauleveritt/customizing_sphinx/tree/master/tests/integration
# and https://github.com/sphinx-doc/sphinx/issues/7008

# stdlib
import sys
from decimal import Decimal
from enum import Enum
from pathlib import Path

# 3rd party
import pytest
import sphinx
from bs4 import BeautifulSoup, NavigableString  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore
from sphinx_toolbox.testing import HTMLRegressionFixture

# this package
from enum_tools.autoenum import EnumDocumenter

NEW_ENUM_REPR = sys.version_info >= (3, 11)

xfail_311 = pytest.mark.xfail(
		reason="Python 3.11 behaviour has not been finalised yet.",
		condition=sys.version_info[:2] == (3, 11) and sys.version_info.releaselevel == "alpha"
		)


@pytest.mark.parametrize("obj", [
		"abcdefg",
		b"abcdefg",
		b"\x00\x01",
		12345,
		123.45,
		Decimal(123.45),
		Path('.'),
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

return_arrow = " → "


def preprocess_soup(soup: BeautifulSoup):

	if sphinx.version_info >= (3, 5):  # pragma: no cover
		for em in soup.select("em.property"):
			child = ''.join(c.string for c in em.contents)
			for c in em.children:
				c.extract()
			em.contents = []
			em.insert(0, child)

		for dl in soup.select("dl.py.method dt"):  # .sig.sig-object.py
			if return_arrow in dl.contents:
				arrow_idx = dl.contents.index(return_arrow)
				dl.contents[arrow_idx] = NavigableString(
						dl.contents[arrow_idx] + dl.contents[arrow_idx + 1].contents[0]
						)
				dl.contents[arrow_idx + 1].extract()

	for dt in soup.select("span.pre"):
		dt.replace_with_children()

	for dt in soup.select("span.sig-return"):
		dt.replace_with(NavigableString(dt.get_text()))


@xfail_311
@pytest.mark.parametrize(
		"page", [
				"index.html",
				], indirect=True
		)
def test_index(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "autoenum Demo" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.findAll("dl"):
		if "enum" not in class_["class"]:
			continue

		if class_count == 0:
			assert class_.find("dt")["id"] == "enum_tools.demo.People"
			assert class_.find("dd").findAll('p')[0].contents[0] == "An enumeration of people."
		elif class_count == 1:
			assert class_.find("dt")["id"] == "enum_tools.demo.NoMethods"
			assert class_.find("dd").findAll('p')[0].contents[0] == "An enumeration of people without any methods."

		tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
		assert str(class_.find("dd").findAll('p')[1].contents[0]) == tag
		assert class_.find("dd").findAll('p')[2].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.findAll("dl"):
			if "attribute" not in attr["class"]:
				continue

			if class_count == 0:
				class_name = "People"
			else:
				class_name = "NoMethods"

			if attr_count == 0:
				assert attr.find("dt")["id"] == f"enum_tools.demo.{class_name}.Bob"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == f" = {class_name}.Bob"
				else:
					assert attr.find("dt").em.contents[0] == f" = <{class_name}.Bob: 1>"

				assert str(attr.find("dd").contents[0]) == "<p>A person called Bob</p>"

			elif attr_count == 1:
				assert attr.find("dt")["id"] == f"enum_tools.demo.{class_name}.Alice"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == f" = {class_name}.Alice"
				else:
					assert attr.find("dt").em.contents[0] == f" = <{class_name}.Alice: 2>"

				assert str(attr.find("dd").contents[0]) == "<p>A person called Alice</p>"

			elif attr_count == 2:
				assert attr.find("dt")["id"] == f"enum_tools.demo.{class_name}.Carol"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == f" = {class_name}.Carol"
				else:
					assert attr.find("dt").em.contents[0] == f" = <{class_name}.Carol: 3>"

				if class_count == 0:
					assert str(attr.find("dd").contents[0]) == "<p>A person called Carol.</p>"
					assert str(attr.find("dd").contents[1]) == '\n'
					assert str(attr.find("dd").contents[2]) == "<p>This is a multiline docstring.</p>"
				else:
					assert str(attr.find("dd").contents[0]) == "<p>A person called Carol</p>"

			elif attr_count == 3:
				assert attr.find("dt")["id"] == f"enum_tools.demo.{class_name}.Dennis"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == f" = {class_name}.Dennis"
				else:
					assert attr.find("dt").em.contents[0] == f" = <{class_name}.Dennis: 4>"

				assert str(attr.find("dd").contents[0]) == "<p>A person called Dennis</p>"

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@xfail_311
@pytest.mark.parametrize(
		"page", [
				"flag.html",
				], indirect=True
		)
def test_flag(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "autoenum Demo - Flag" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.findAll("dl"):
		if "flag" not in class_["class"]:
			continue

		if class_count == 0:
			assert class_.find("dt")["id"] == "enum_tools.demo.StatusFlags"
		elif class_count == 1:
			assert class_.find("dt")["id"] == "id0"

		assert class_.find("dd").findAll('p')[0].contents[0] == "An enumeration of status codes."

		tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
		assert str(class_.find("dd").findAll('p')[1].contents[0]) == tag
		assert class_.find("dd").findAll('p')[2].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.findAll("dl"):
			if "attribute" not in attr["class"]:
				continue

			if attr_count == 0:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.StatusFlags.Running"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id1"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == " = StatusFlags.Running"
				else:
					assert attr.find("dt").em.contents[0] == " = <StatusFlags.Running: 1>"

				assert str(attr.find("dd").contents[0]) == "<p>The system is running.</p>"
			elif attr_count == 1:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.StatusFlags.Stopped"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id2"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == " = StatusFlags.Stopped"
				else:
					assert attr.find("dt").em.contents[0] == " = <StatusFlags.Stopped: 2>"

				assert str(attr.find("dd").contents[0]) == "<p>The system has stopped.</p>"
			elif attr_count == 2:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.StatusFlags.Error"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id3"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == " = StatusFlags.Error"
				else:
					assert attr.find("dt").em.contents[0] == " = <StatusFlags.Error: 4>"

				assert str(attr.find("dd").contents[0]) == "<p>An error has occurred.</p>"

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@xfail_311
@pytest.mark.parametrize(
		"page", [
				"no-member-doc.html",
				], indirect=True
		)
def test_no_member_doc(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "autoenum Demo - Members without docstrings" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.findAll("dl"):
		if "enum" not in class_["class"]:
			continue

		assert class_.find("dt")["id"] == "enum_tools.demo.NoMemberDoc"
		assert class_.find("dd").findAll('p')[0].contents[
				0] == "An enumeration of people without any member docstrings."

		if class_count == 0:
			tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
			assert str(class_.find("dd").findAll('p')[1].contents[0]) == tag
			assert class_.find("dd").findAll('p')[2].contents[0] == "Valid values are as follows:"
		else:
			assert class_.find("dd").findAll('p')[1].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.findAll("dl"):
			if "attribute" not in attr["class"]:
				continue

			if attr_count == 0:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.NoMemberDoc.Bob"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id1"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == " = NoMemberDoc.Bob"
				else:
					assert attr.find("dt").em.contents[0] == " = <NoMemberDoc.Bob: 1>"

				assert not attr.find("dd").contents
			elif attr_count == 1:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.NoMemberDoc.Alice"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id2"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == " = NoMemberDoc.Alice"
				else:
					assert attr.find("dt").em.contents[0] == " = <NoMemberDoc.Alice: 2>"

				assert not attr.find("dd").contents
			elif attr_count == 2:
				if class_count == 0:
					assert attr.find("dt")["id"] == "enum_tools.demo.NoMemberDoc.Carol"
				elif class_count == 1:
					assert attr.find("dt")["id"] == "id3"

				if NEW_ENUM_REPR:
					assert attr.find("dt").em.contents[0] == " = NoMemberDoc.Carol"
				else:
					assert attr.find("dt").em.contents[0] == " = <NoMemberDoc.Carol: 3>"

				assert not attr.find("dd").contents

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 1
