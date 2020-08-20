# stdlib
import pathlib

# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from sphinx.testing.path import path

pytest_plugins = 'sphinx.testing.fixtures'


@pytest.fixture(scope='session')
def rootdir():
	rdir = pathlib.Path(__file__).parent.absolute() / "doc-test"
	if not (rdir / "test-root").is_dir():
		(rdir / "test-root").mkdir(parents=True)
	return path(rdir)


@pytest.fixture()
def content(app):
	app.build()
	yield app


@pytest.fixture()
def page(content, request) -> BeautifulSoup:
	pagename = request.param
	c = (content.outdir / pagename).read_text()

	yield BeautifulSoup(c, 'html5lib')
