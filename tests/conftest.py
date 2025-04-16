# stdlib
import pathlib
import sys
import types
from typing import Dict, Iterator, List, cast

# 3rd party
import pytest
import sphinx
from bs4 import BeautifulSoup  # type: ignore[import-untyped]
from sphinx.application import Sphinx

if sys.version_info >= (3, 10):
	types.Union = types.UnionType

if sphinx.version_info >= (7, 2):
	path = pathlib.Path
else:
	# 3rd party
	from sphinx.testing.path import path  # type: ignore[assignment]

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
	c = c.replace("Â¶", '¶')
	c = c.replace("â€™", '’')

	soup = BeautifulSoup(c, "html5lib")

	for meta in cast(List[Dict], soup.find_all("meta")):
		if meta.get("content", '') == "width=device-width, initial-scale=0.9, maximum-scale=0.9":
			meta.extract()  # type: ignore[attr-defined]

	return soup
