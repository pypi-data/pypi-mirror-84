from __future__ import annotations

import typing

T = typing.TypeVar("T")
PT = typing.TypeVar("PT", bound="Parsable")

# cls: typing.Type[PT]
# tokens: typing.Union[typing.Sequence[T_contra], T_contra]
# line: int
# returns: PT
ParseFunction = typing.Callable[
    [typing.Type[PT], typing.Union[typing.Sequence[T], T], int], PT
]
ParseMethod = typing.Callable[[typing.Union[typing.Sequence[T], T], int], PT]

TPF = typing.TypeVar("TPF", bound=ParseFunction)


class Parsable:
    parse_function: typing.ClassVar[typing.Optional[ParseFunction]] = None

    @classmethod
    def make_parse_function(cls, function: TPF) -> TPF:
        cls.parse_function = function
        return function

    @classmethod
    def parse(
        cls: typing.Type[PT],
        tokens: typing.Union[typing.Sequence[typing.Any], typing.Any],
        line: int,
    ) -> PT:
        if cls.parse_function is None:
            decorator = f"{cls.__name__}.make_parse_function"
            msg = (
                "parse method not implemented; "
                f"specify parse function using {decorator} decorator"
            )
            raise NotImplementedError(msg)
        if not isinstance(tokens, typing.Sequence):
            tokens = [tokens]
        return cls.parse_function(cls, tokens, line)
