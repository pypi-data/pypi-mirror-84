import pytest


from .dummy import Dummy
from .util import _test_valid_args, _test_invalid_args, Value, Values


class Enum(Dummy):
    def __init__(self, *values, invalids=None):
        super().__init__()
        if len(values) == 0:
            raise ValueError("Must provide at least one value for enum values.")
        if len(values) != len(set(values)):
            raise ValueError("Enum values must be unique.")
        self._valids_ = list(values)
        self._invalids_ = invalids if invalids else []
    
    def _valids(self):
        return Values(self._valids_)
    
    def _invalids(self):
        invalids = [
            (v, "invalid enum value: {}".format(v))
            for v in self._invalids_
        ]
        return Values(invalids)
    
    def valid(self, value, raise_error=False):
        if value not in self._valids_:
            if raise_error:
                raise ValueError("{} not a valid enum value, must be one of {}".format(
                    value, self._valids_
                ))
                return False
        return True
    
    def __str__(self):
        return "Enum: {}".format(self._valids_)


def test_enum():
    _test_valid_args(Enum, [
        [1], [1, "2", 33]
    ])

    _test_invalid_args(Enum, [
        [], [1, 2, 1], [3, 3]
    ])

    assert Enum(1, 2, 3).valids(3) == [1, 2, 3]
    assert Enum(1, 2, invalids=[3, 4]).invalids(2) == [3, 4]
    for i in range(1,10):
        assert Enum(*list(range(1,i+1))).valid(i, True), i
    for i in range(1,10):
        with pytest.raises(ValueError):
            Enum(*list(range(i+1,i+5))).valid(i, True), i
