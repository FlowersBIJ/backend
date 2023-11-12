from typing import Optional, Any, TypeVar, Type, Sequence, NoReturn

from adaptix import Retort
from psycopg import pq, InterfaceError
from psycopg.cursor import BaseCursor
from psycopg.pq.abc import PGresult
from psycopg.rows import BaseRowFactory, RowMaker

COMMAND_OK = pq.ExecStatus.COMMAND_OK
TUPLES_OK = pq.ExecStatus.TUPLES_OK
SINGLE_TUPLE = pq.ExecStatus.SINGLE_TUPLE
T = TypeVar("T", covariant=True)


def _get_names(cursor: BaseCursor[Any, Any]) -> Optional[list[str]]:
    res = cursor.pgresult
    if not res:
        return None

    nfields = _get_nfields(res)
    if nfields is None:
        return None

    enc = cursor._encoding
    return [
        res.fname(i).decode(enc) for i in range(nfields)  # type: ignore[union-attr]
    ]


def no_result(values: Sequence[Any]) -> NoReturn:
    """A `RowMaker` that always fail.

    It can be used as return value for a `RowFactory` called with no result.
    Note that the `!RowFactory` *will* be called with no result, but the
    resulting `!RowMaker` never should.
    """
    raise InterfaceError("the cursor doesn't have a result")


def _get_nfields(res: PGresult) -> Optional[int]:
    """
    Return the number of columns in a result, if it returns tuples else None

    Take into account the special case of results with zero columns.
    """
    nfields = res.nfields

    if (
            res.status == TUPLES_OK
            or res.status == SINGLE_TUPLE
            # "describe" in named cursors
            or (res.status == COMMAND_OK and nfields)
    ):
        return nfields
    else:
        return None


def retort_row(cls: Type[T], retort: Retort) -> BaseRowFactory[T]:
    def retort_row_(cursor: BaseCursor[Any, Any]) -> RowMaker[T]:
        names = _get_names(cursor)
        if names is None:
            return no_result

        def retort_row__(values: Sequence[Any]) -> T:
            return retort.load(
                values, cls
            )

        return retort_row__

    return retort_row_
