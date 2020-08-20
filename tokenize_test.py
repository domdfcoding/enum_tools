# stdlib
import tokenize
from io import StringIO
from pprint import pprint

tokens = tokenize.generate_tokens(StringIO('foo = "abcdefg"  # doc: a docstring').readline)
pprint(list(tokens))
