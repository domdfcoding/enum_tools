# Based on https://github.com/pauleveritt/customizing_sphinx/tree/master/tests/integration
# and https://github.com/sphinx-doc/sphinx/issues/7008

# stdlib
import sys
from decimal import Decimal
from enum import Enum
from pathlib import Path

# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture  # type: ignore
from sphinx_toolbox.testing import HTMLRegressionFixture

# this package
from enum_tools.autoenum import EnumDocumenter

NEW_ENUM_REPR = sys.version_info >= (3, 11)


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


@pytest.mark.parametrize(
		"page", [
				"index.html",
				], indirect=True
		)
def test_index(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "autoenum Demo" == title

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

		assert str(class_.find("dd").findAll('p')[1].contents[0]) == (
				'<code class="xref py py-class docutils literal notranslate">'
				'<span class="pre">int</span></code>'
				)
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

				assert str(attr.find("dd").contents[0]) == "<p>A person called Carol</p>"

			attr_count += 1

		class_count += 1

	# print(page)

	assert class_count == 2


@pytest.mark.parametrize(
		"page", [
				"flag.html",
				], indirect=True
		)
def test_flag(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "autoenum Demo - Flag" == title

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

		assert str(class_.find("dd").findAll('p')[1].contents[0]) == (
				'<code class="xref py py-class docutils literal notranslate">'
				'<span class="pre">int</span></code>'
				)
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


@pytest.mark.parametrize(
		"page", [
				"no-member-doc.html",
				], indirect=True
		)
def test_no_member_doc(page: BeautifulSoup, html_regression: HTMLRegressionFixture):
	# Make sure the page title is what you expect
	title = page.find("h1").contents[0].strip()
	assert "autoenum Demo - Members without docstrings" == title

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
			assert str(class_.find("dd").findAll('p')[1].contents[0]) == (
					'<code class="xref py py-class docutils literal notranslate">'
					'<span class="pre">int</span></code>'
					)
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
