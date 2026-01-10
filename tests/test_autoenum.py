# Based on https://github.com/pauleveritt/customizing_sphinx/tree/master/tests/integration
# and https://github.com/sphinx-doc/sphinx/issues/7008

# stdlib
import sys
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import cast

# 3rd party
import pytest
import sphinx
from bs4 import BeautifulSoup, NavigableString, Tag
from sphinx.application import Sphinx
from sphinx_toolbox.testing import HTMLRegressionFixture

# this package
from enum_tools.autoenum import EnumDocumenter

NEW_ENUM_REPR = sys.version_info >= (3, 14)

xfail_312 = pytest.mark.xfail(
		reason="Python 3.14 behaviour has not been finalised yet.",
		condition=sys.version_info[:2] == (3, 14) and sys.version_info.releaselevel == "alpha",
		)


@pytest.mark.parametrize(
		"obj",
		[
				"abcdefg",
				b"abcdefg",
				b"\x00\x01",
				12345,
				123.45,
				Decimal(123.45),
				Path('.'),
				],
		)
def test_cannot_document_member(obj: object):
	assert not EnumDocumenter.can_document_member(obj, '', True, '')


class MyEnum(Enum):
	foo = 1
	bar = 2


def test_can_document_member():
	assert EnumDocumenter.can_document_member(MyEnum, '', True, '')


def test(app: Sphinx) -> None:
	# app is a Sphinx application object for default sphinx project (`tests/roots/test-root`).
	app.build()


# @pytest.mark.sphinx(buildername='latex')
# def test_latex(app):
# 	# latex builder is chosen here.
# 	app.build()

# pytestmark = pytest.mark.sphinx('html', testroot='root')

return_arrow = " → "


def preprocess_soup(soup: BeautifulSoup) -> None:

	if sphinx.version_info >= (3, 5):  # pragma: no cover
		for em in soup.select("em.property"):
			child = ''.join(c.string for c in em.contents)  # type: ignore[attr-defined]
			for c in em.children:
				c.extract()
			em.contents = []
			em.insert(0, child)

		for dl in soup.select("dl.py.method dt"):  # .sig.sig-object.py
			if return_arrow in dl.contents:
				arrow_idx = dl.contents.index(return_arrow)  # type: ignore[arg-type]
				contents = dl.contents
				string = contents[arrow_idx] + contents[arrow_idx + 1].contents[0]  # type: ignore[attr-defined]
				contents[arrow_idx] = NavigableString(string)
				contents[arrow_idx + 1].extract()

	for dt in soup.select("span.pre"):
		dt.replace_with_children()

	for dt in soup.select("span.sig-return"):
		dt.replace_with(NavigableString(dt.get_text()))

	for div in soup.find_all("script"):
		if cast(Tag, div).get("src"):
			div["src"] = div["src"].split("?v=")[0]  # type: ignore[union-attr]
			print(div["src"])

	for meta in soup.find_all("meta"):
		if meta.get("content", '') == "width=device-width, initial-scale=0.9, maximum-scale=0.9":
			meta.extract()

	for div in soup.select("div.related"):
		if div["aria-label"] == "Related":
			div.extract()


def get_page_h1(page: BeautifulSoup) -> str:
	h1 = page.find("h1")
	assert h1 is not None
	contents = h1.contents
	assert contents is not None
	title = cast(str, contents[0]).strip()
	return title


@xfail_312
@pytest.mark.parametrize(
		"page",
		[
				"index.html",
				],
		indirect=True,
		)
def test_index(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = get_page_h1(page)
	assert "autoenum Demo" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.find_all("dl"):
		if "enum" not in class_["class"]:
			continue

		dd = class_.find("dd")
		assert dd is not None
		p = dd.find_all('p')
		assert p is not None
		dt = class_.find("dt")
		assert dt is not None

		if class_count == 0:
			assert dt["id"] == "enum_tools.demo.People"
			assert p[0].contents[0] == "An enumeration of people."
		elif class_count == 1:
			assert dt["id"] == "enum_tools.demo.NoMethods"
			expected = "An enumeration of people without any methods."
			assert p[0].contents[0] == expected

		tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
		assert str(p[1].contents[0]) == tag
		assert p[2].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.find_all("dl"):
			attr = cast(Tag, attr)
			if "attribute" not in attr["class"]:
				continue

			if class_count == 0:
				class_name = "People"
			else:
				class_name = "NoMethods"

			dt = attr.find("dt")
			assert dt is not None
			em = dt.em
			assert em is not None
			dd = attr.find("dd")
			assert dd is not None

			if attr_count == 0:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Bob"

				if NEW_ENUM_REPR:
					assert em.contents[0] == f" = {class_name}.Bob"
				else:
					assert em.contents[0] == f" = <{class_name}.Bob: 1>"

				assert str(dd.contents[0]) == "<p>A person called Bob</p>"

			elif attr_count == 1:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Alice"

				if NEW_ENUM_REPR:
					assert em.contents[0] == f" = {class_name}.Alice"
				else:
					assert em.contents[0] == f" = <{class_name}.Alice: 2>"

				assert str(dd.contents[0]) == "<p>A person called Alice</p>"

			elif attr_count == 2:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Carol"

				if NEW_ENUM_REPR:
					assert em.contents[0] == f" = {class_name}.Carol"
				else:
					assert em.contents[0] == f" = <{class_name}.Carol: 3>"

				if class_count == 0:
					contents = dd.contents
					assert str(contents[0]) == "<p>A person called Carol.</p>"
					assert str(contents[1]) == '\n'
					assert str(contents[2]) == "<p>This is a multiline docstring.</p>"
				else:
					assert str(dd.contents[0]) == "<p>A person called Carol</p>"

			elif attr_count == 3:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Dennis"

				if NEW_ENUM_REPR:
					assert em.contents[0] == f" = {class_name}.Dennis"
				else:
					assert em.contents[0] == f" = <{class_name}.Dennis: 4>"

				assert str(dd.contents[0]) == "<p>A person called Dennis</p>"

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@xfail_312
@pytest.mark.parametrize("page", ["flag.html"], indirect=True)
def test_flag(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = get_page_h1(page)
	assert "autoenum Demo - Flag" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.find_all("dl"):
		if "flag" not in class_["class"]:
			continue

		dt = class_.find("dt")
		assert dt is not None

		if class_count == 0:
			assert dt["id"] == "enum_tools.demo.StatusFlags"
		elif class_count == 1:
			assert dt["id"] == "id0"

		dd = class_.find("dd")
		assert dd is not None
		ps = dd.find_all('p')

		assert ps[0].contents[0] == "An enumeration of status codes."

		tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
		assert str(ps[1].contents[0]) == tag
		assert ps[2].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.find_all("dl"):
			attr = cast(Tag, attr)
			if "attribute" not in attr["class"]:
				continue

			dt = attr.find("dt")
			assert dt is not None
			assert dt.em is not None
			dd = attr.find("dd")
			assert dd is not None
			assert dd.contents is not None

			if attr_count == 0:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.StatusFlags.Running"
				elif class_count == 1:
					assert dt["id"] == "id1"

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = StatusFlags.Running"
				else:
					assert dt.em.contents[0] == " = <StatusFlags.Running: 1>"

				assert str(dd.contents[0]) == "<p>The system is running.</p>"
			elif attr_count == 1:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.StatusFlags.Stopped"
				elif class_count == 1:
					assert dt["id"] == "id2"

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = StatusFlags.Stopped"
				else:
					assert dt.em.contents[0] == " = <StatusFlags.Stopped: 2>"

				assert str(dd.contents[0]) == "<p>The system has stopped.</p>"
			elif attr_count == 2:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.StatusFlags.Error"
				elif class_count == 1:
					assert dt["id"] == "id3"

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = StatusFlags.Error"
				else:
					assert dt.em.contents[0] == " = <StatusFlags.Error: 4>"

				assert str(dd.contents[0]) == "<p>An error has occurred.</p>"

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@xfail_312
@pytest.mark.parametrize("page", ["no-member-doc.html"], indirect=True)
def test_no_member_doc(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = get_page_h1(page)
	assert "autoenum Demo - Members without docstrings" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.find_all("dl"):
		if "enum" not in class_["class"]:
			continue

		dd = class_.find("dd")
		assert dd is not None
		dt = class_.find("dt")
		assert dt is not None
		p = dd.find_all('p')
		assert p is not None

		assert dt["id"] == "enum_tools.demo.NoMemberDoc"
		expected = "An enumeration of people without any member docstrings."
		assert dd.find_all('p')[0].contents[0] == expected

		if class_count == 0:
			tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
			assert str(dd.find_all('p')[1].contents[0]) == tag
			assert dd.find_all('p')[2].contents[0] == "Valid values are as follows:"
		else:
			assert dd.find_all('p')[1].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.find_all("dl"):
			attr = cast(Tag, attr)
			if "attribute" not in attr["class"]:
				continue

			dt = attr.find("dt")
			assert dt is not None
			em = dt.em
			assert em is not None
			dd = attr.find("dd")
			assert dd is not None

			if attr_count == 0:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.NoMemberDoc.Bob"
				elif class_count == 1:
					assert dt["id"] == "id1"

				if NEW_ENUM_REPR:
					assert em.contents[0] == " = NoMemberDoc.Bob"
				else:
					assert em.contents[0] == " = <NoMemberDoc.Bob: 1>"

				assert not dd.contents
			elif attr_count == 1:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.NoMemberDoc.Alice"
				elif class_count == 1:
					assert dt["id"] == "id2"

				if NEW_ENUM_REPR:
					assert em.contents[0] == " = NoMemberDoc.Alice"
				else:
					assert em.contents[0] == " = <NoMemberDoc.Alice: 2>"

				assert not dd.contents
			elif attr_count == 2:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.NoMemberDoc.Carol"
				elif class_count == 1:
					assert dt["id"] == "id3"

				if NEW_ENUM_REPR:
					assert em.contents[0] == " = NoMemberDoc.Carol"
				else:
					assert em.contents[0] == " = <NoMemberDoc.Carol: 3>"

				assert not dd.contents

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 1
