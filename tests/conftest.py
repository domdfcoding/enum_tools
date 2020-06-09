import shutil
import tempfile

tempdir = tempfile.mkdtemp()


def teardown_module(module):
	shutil.rmtree(tempdir, True)
