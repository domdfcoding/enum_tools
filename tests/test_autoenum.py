# Based on https://github.com/pauleveritt/customizing_sphinx/tree/master/tests/integration
# and https://github.com/sphinx-doc/sphinx/issues/7008

# stdlib
import sys
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Dict, List, cast

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
		condition=sys.version_info[:2] == (3, 14) and sys.version_info.releaselevel == "alpha"
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
			div["src"] = div["src"].split("?v=")[0]  # type: ignore[union-attr,index]
			print(div["src"])  # type: ignore[index]

	for meta in cast(List[Dict], soup.find_all("meta")):
		if meta.get("content", '') == "width=device-width, initial-scale=0.9, maximum-scale=0.9":
			meta.extract()  # type: ignore[attr-defined]

	for div in soup.select("div.related"):
		if div["aria-label"] == "Related":
			div.extract()


@xfail_312
@pytest.mark.parametrize(
		"page", [
				"index.html",
				], indirect=True
		)
def test_index(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()  # type: ignore[union-attr]
	assert "autoenum Demo" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.find_all("dl"):
		if "enum" not in class_["class"]:  # type: ignore[index]
			continue

		dd = class_.find("dd")  # type: ignore[union-attr]
		if class_count == 0:
			assert class_.find("dt")["id"] == "enum_tools.demo.People"  # type: ignore[union-attr,index]
			assert dd.find_all('p')[0].contents[0] == "An enumeration of people."  # type: ignore[union-attr]
		elif class_count == 1:
			assert class_.find("dt")["id"] == "enum_tools.demo.NoMethods"  # type: ignore[union-attr,index]
			expected = "An enumeration of people without any methods."
			assert dd.find_all('p')[0].contents[0] == expected  # type: ignore[union-attr]

		tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
		assert str(dd.find_all('p')[1].contents[0]) == tag  # type: ignore[union-attr]
		assert dd.find_all('p')[2].contents[0] == "Valid values are as follows:"  # type: ignore[union-attr]

		attr_count = 0

		for attr in class_.find_all("dl"):  # type: ignore[union-attr]
			attr = cast(Tag, attr)
			if "attribute" not in attr["class"]:
				continue

			if class_count == 0:
				class_name = "People"
			else:
				class_name = "NoMethods"

			dt = attr.find("dt")
			dd = attr.find("dd")
			if attr_count == 0:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Bob"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == f" = {class_name}.Bob"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == f" = <{class_name}.Bob: 1>"  # type: ignore[union-attr]

				assert str(dd.contents[0]) == "<p>A person called Bob</p>"  # type: ignore[union-attr]

			elif attr_count == 1:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Alice"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == f" = {class_name}.Alice"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == f" = <{class_name}.Alice: 2>"  # type: ignore[union-attr]

				assert str(dd.contents[0]) == "<p>A person called Alice</p>"  # type: ignore[union-attr]

			elif attr_count == 2:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Carol"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == f" = {class_name}.Carol"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == f" = <{class_name}.Carol: 3>"  # type: ignore[union-attr]

				if class_count == 0:
					contents = dd.contents  # type: ignore[union-attr]
					assert str(contents[0]) == "<p>A person called Carol.</p>"
					assert str(contents[1]) == '\n'
					assert str(contents[2]) == "<p>This is a multiline docstring.</p>"
				else:
					assert str(dd.contents[0]) == "<p>A person called Carol</p>"  # type: ignore[union-attr]

			elif attr_count == 3:
				assert dt["id"] == f"enum_tools.demo.{class_name}.Dennis"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == f" = {class_name}.Dennis"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == f" = <{class_name}.Dennis: 4>"  # type: ignore[union-attr]

				assert str(dd.contents[0]) == "<p>A person called Dennis</p>"  # type: ignore[union-attr]

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@xfail_312
@pytest.mark.parametrize("page", ["flag.html"], indirect=True)
def test_flag(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()  # type: ignore[union-attr]
	assert "autoenum Demo - Flag" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.find_all("dl"):
		if "flag" not in class_["class"]:  # type: ignore[index]
			continue

		if class_count == 0:
			assert class_.find("dt")["id"] == "enum_tools.demo.StatusFlags"  # type: ignore[union-attr,index]
		elif class_count == 1:
			assert class_.find("dt")["id"] == "id0"  # type: ignore[union-attr,index]

		ps = class_.find("dd").find_all('p')  # type: ignore[union-attr]
		assert ps[0].contents[0] == "An enumeration of status codes."

		tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
		assert str(ps[1].contents[0]) == tag
		assert ps[2].contents[0] == "Valid values are as follows:"

		attr_count = 0

		for attr in class_.find_all("dl"):  # type: ignore[union-attr]
			attr = cast(Tag, attr)
			if "attribute" not in attr["class"]:
				continue

			dt = attr.find("dt")
			dd = attr.find("dd")
			if attr_count == 0:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.StatusFlags.Running"  # type: ignore[index]
				elif class_count == 1:
					assert dt["id"] == "id1"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = StatusFlags.Running"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == " = <StatusFlags.Running: 1>"  # type: ignore[union-attr]

				assert str(dd.contents[0]) == "<p>The system is running.</p>"  # type: ignore[union-attr]
			elif attr_count == 1:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.StatusFlags.Stopped"  # type: ignore[index]
				elif class_count == 1:
					assert dt["id"] == "id2"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = StatusFlags.Stopped"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == " = <StatusFlags.Stopped: 2>"  # type: ignore[union-attr]

				assert str(dd.contents[0]) == "<p>The system has stopped.</p>"  # type: ignore[union-attr]
			elif attr_count == 2:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.StatusFlags.Error"  # type: ignore[index]
				elif class_count == 1:
					assert dt["id"] == "id3"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = StatusFlags.Error"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == " = <StatusFlags.Error: 4>"  # type: ignore[union-attr]

				assert str(dd.contents[0]) == "<p>An error has occurred.</p>"  # type: ignore[union-attr]

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@xfail_312
@pytest.mark.parametrize("page", ["no-member-doc.html"], indirect=True)
def test_no_member_doc(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()  # type: ignore[union-attr]
	assert "autoenum Demo - Members without docstrings" == title

	preprocess_soup(page)

	html_regression.check(page, jinja2=True)

	# Now test the directive

	class_count = 0

	for class_ in page.find_all("dl"):
		if "enum" not in class_["class"]:  # type: ignore[index]
			continue

		dd = class_.find("dd")  # type: ignore[union-attr]
		assert class_.find("dt")["id"] == "enum_tools.demo.NoMemberDoc"  # type: ignore[union-attr,index]
		expected = "An enumeration of people without any member docstrings."
		assert dd.find_all('p')[0].contents[0] == expected  # type: ignore[union-attr]

		if class_count == 0:
			tag = '<code class="xref py py-class docutils literal notranslate">int</code>'
			assert str(dd.find_all('p')[1].contents[0]) == tag  # type: ignore[union-attr]
			assert dd.find_all('p')[2].contents[0] == "Valid values are as follows:"  # type: ignore[union-attr]
		else:
			assert dd.find_all('p')[1].contents[0] == "Valid values are as follows:"  # type: ignore[union-attr]

		attr_count = 0

		for attr in class_.find_all("dl"):  # type: ignore[union-attr]
			attr = cast(Tag, attr)
			if "attribute" not in attr["class"]:
				continue

			dt = attr.find("dt")
			if attr_count == 0:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.NoMemberDoc.Bob"  # type: ignore[index]
				elif class_count == 1:
					assert dt["id"] == "id1"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = NoMemberDoc.Bob"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == " = <NoMemberDoc.Bob: 1>"  # type: ignore[union-attr]

				assert not attr.find("dd").contents  # type: ignore[union-attr]
			elif attr_count == 1:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.NoMemberDoc.Alice"  # type: ignore[index]
				elif class_count == 1:
					assert dt["id"] == "id2"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = NoMemberDoc.Alice"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == " = <NoMemberDoc.Alice: 2>"  # type: ignore[union-attr]

				assert not attr.find("dd").contents  # type: ignore[union-attr]
			elif attr_count == 2:
				if class_count == 0:
					assert dt["id"] == "enum_tools.demo.NoMemberDoc.Carol"  # type: ignore[index]
				elif class_count == 1:
					assert dt["id"] == "id3"  # type: ignore[index]

				if NEW_ENUM_REPR:
					assert dt.em.contents[0] == " = NoMemberDoc.Carol"  # type: ignore[union-attr]
				else:
					assert dt.em.contents[0] == " = <NoMemberDoc.Carol: 3>"  # type: ignore[union-attr]

				assert not attr.find("dd").contents  # type: ignore[union-attr]

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 1
