# stdlib
import pathlib
import sys
import types
from typing import Iterator

# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from sphinx.application import Sphinx
from sphinx.testing.path import path

if sys.version_info >= (3, 10):
	types.Union = types.UnionType

pytest_plugins = ("coincidence", "sphinx.testing.fixtures", "sphinx_toolbox.testing")


@pytest.fixture(scope="session")
def rootdir() -> path:
	rdir = pathlib.Path(__file__).parent.absolute() / "doc-test"
	if not (rdir / "test-root").is_dir():
		(rdir / "test-root").mkdir(parents=True)
	return path(rdir)


@pytest.fixture()
def content(app: Sphinx) -> Iterator[Sphinx]:
	app.build()
	yield app


@pytest.fixture()
def page(content, request) -> BeautifulSoup:  # noqa: MAN001
	pagename = request.param
	c = (content.outdir / pagename).read_text()

	yield BeautifulSoup(c, "html5lib")
