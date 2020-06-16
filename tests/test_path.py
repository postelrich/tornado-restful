from unittest.mock import patch, MagicMock

import pytest

from tornado_restful.path import PathArg, RestFunction


def test_patharg_init():
    p = PathArg('int', 'foo')
    assert p.type_ == int
    assert p.name == 'foo'
    assert p.optional is False
    p = PathArg('int', 'foo', optional=1)
    assert p.optional is True
    with pytest.raises(TypeError):
        PathArg(1, 'x')


def test_patharg_parse():
    p = PathArg('int', 'foo')
    assert p.parse('1') == 1
    with pytest.raises(ValueError):
        p.parse('x')


def test_restfunction_init(monkeypatch):
    afp = MagicMock()
    ptrp = MagicMock()
    monkeypatch.setattr('tornado_restful.path.RestFunction.args_from_path', afp)
    monkeypatch.setattr('tornado_restful.path.RestFunction.path_to_regex_path', ptrp)
    afp.return_value = list()
    r = RestFunction('func', 'path', 'GET')
    assert r.f == 'func'
    assert r.path == 'path'
    assert r.method == 'GET'
    afp.assert_called_once_with(r.path)
    ptrp.assert_called_once_with(r.args, r.path)


def test_restfunction_args_from_path():
    assert RestFunction.args_from_path('/<int:foo>') == [PathArg('int', 'foo')]
    assert RestFunction.args_from_path('/<int:foo>/bar/<str:bizz>') == [PathArg('int', 'foo'),
                                                                        PathArg('str', 'bizz')]
    assert RestFunction.args_from_path('/<int:foo>/bar/<str:bizz:optional>') == [PathArg('int', 'foo'),
                                                                                 PathArg('str', 'bizz', optional=True)]


def test_restfunction_args_from_path_raises_with_optional_before_last_arg():
    with pytest.raises(AssertionError):
        RestFunction.args_from_path('/<int:foo:optional>/bar/<str:bizz>')


def test_restfunction_call():
    def foo(handler, x, y):
        return x + y
    r = RestFunction(foo, '/<int:x>/<int:y>', 'GET')
    assert r(None, 1, 2) == 3
