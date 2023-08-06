from faker import Faker as Faker_
import pytest


from .dummy import Dummy
from .util import _test_valid_args, _test_invalid_args, Value, Values


class Faker(Dummy):
    BASIC_FAKER = Faker_()

    def __init__(self, kind, locales=None, invalids=None,
                 args=None, kwargs=None,
                 post_process=None):
        super().__init__()
        self.kind = kind
        self.locales = locales if locales else []
        self.args = args if args else []
        self.kwargs = kwargs if kwargs else {}
        self.post_process = post_process if post_process else lambda x: x
        if self.locales and len(self.locales) > 0:
            self.faker = Faker_(self.locales)
        else:
            self.faker = Faker.BASIC_FAKER
        if not hasattr(self.faker, kind):
            raise ValueError("faker does not have a property {}".format(kind))
        self._invalids_ = invalids if invalids else []
    
    def _valids(self):
        func = getattr(self.faker, self.kind)
        valid = func(*self.args, **self.kwargs)
        valid = self.post_process(valid)
        return Value(valid)
    
    def _invalids(self):
        if callable(self._invalids_):
            return Values(self._invalids_)
        else:
            invalids = [
                (v, "invalid fake value: {}".format(v))
                for v in self._invalids_
            ]
            return Values(invalids)
    
    def __str__(self):
        return "Faker of {}".format(self.kind)


def test_faker():
    _test_valid_args(Faker, [
        ["url"], ["name"],
        ["first_name", "de_DE"],
        ["last_name", ["de_DE", "en_US"]],
        ["name", None, [1, 1.3, None]],
        ["name", None, [123]],
    ])
    _test_invalid_args(Faker, [
        [], ["qwe"],
    ])
    
    assert len(Faker("name").valids(5)) == 5
    assert len(Faker("name").invalids(5)) == 0
    assert len(Faker("name", invalids=[1, 2, 3]).invalids(5)) == 3
    assert len(Faker("name", invalids=[123]).invalids(6)) == 1
    assert len(Faker("date", args=["%Y-%m-%dT%H:%M:%SZ"]).valids(7)) == 7
    assert len(Faker("date", args=["%Y-%m-%dT%H:%M:%SZ"]).valids(8)) == 8
    
    #for i in range(10):
    #    o = Object(**props)
    #    for v in o.valids():
    #        assert o.valid(v, True)
    #for i in range(10):
    #    o = Object(**props)
    #    for v in o.invalids(1, True):
    #        with pytest.raises(ValueError):
    #            print(v)
    #            o.valid(v, True)
