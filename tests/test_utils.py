# stdlib
import enum
import http

# 3rd party
import pytest

# this package
from enum_tools import StrEnum
from enum_tools.utils import get_base_object, is_enum, is_enum_member, is_flag


@pytest.mark.parametrize(
		"obj, result",
		[
				(enum.Enum, True),
				(http.HTTPStatus, True),
				(http.HTTPStatus.NOT_ACCEPTABLE, False),
				(123, False),
				("abc", False),
				],
		)
def test_is_enum(obj: object, result: bool):
	assert is_enum(obj) == result  # type: ignore[arg-type]


@pytest.mark.parametrize(
		"obj, result",
		[
				(enum.Enum, False),
				(http.HTTPStatus, False),
				(http.HTTPStatus.NOT_ACCEPTABLE, True),
				(123, False),
				("abc", False),
				],
		)
def test_is_enum_member(obj: object, result: bool):
	assert is_enum_member(obj) == result  # type: ignore[arg-type]


class Colours(enum.Flag):
	RED = 1
	BLUE = 2


PURPLE = Colours.RED | Colours.BLUE


@pytest.mark.parametrize(
		"obj, result",
		[
				(enum.Enum, False),
				(http.HTTPStatus, False),
				(http.HTTPStatus.NOT_ACCEPTABLE, False),
				(123, False),
				("abc", False),
				(Colours, True),
				(Colours.RED, False),
				(PURPLE, False),
				],
		)
def test_is_flag(obj: object, result: bool):
	assert is_flag(obj) == result  # type: ignore[arg-type]


def test_get_base_object():
	# TODO: report issue to mypy
	assert get_base_object(enum.Enum) is object  # type: ignore[arg-type]
	assert get_base_object(Colours) is object  # type: ignore[arg-type]
	assert get_base_object(enum.IntFlag) is int  # type: ignore[arg-type]
	assert get_base_object(StrEnum) is str  # type: ignore[arg-type]

	with pytest.raises(TypeError, match="not an Enum"):
		get_base_object("abc")  # type: ignore[arg-type]

	with pytest.raises(TypeError, match="not an Enum"):
		get_base_object(123)  # type: ignore[arg-type]

	with pytest.raises(TypeError, match="not an Enum"):
		get_base_object(str)  # type: ignore[arg-type]

	with pytest.raises(TypeError, match="not an Enum"):
		get_base_object(int)  # type: ignore[arg-type]
