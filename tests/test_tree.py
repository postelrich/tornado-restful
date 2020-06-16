import pytest

from tornado_restful.path import RestFunction
from tornado_restful.tree import Step, PathDispatcher


def test_step_init():
    s = Step('path', 'part')
    assert s.path == 'path'
    assert s.part == 'part'


def test_pathdispatcher_init():
    p = PathDispatcher()
    assert isinstance(p.registry, Step)
    assert p.registry.path == '/'
    assert p.registry.part == '/'
    assert p.regex_paths == list()


def test_pathdispatcher_find():
    assert PathDispatcher._find([], 'x') == ([], 'x')
    s1 = Step('/widgets', 'widgets')
    s = Step('/', 'GET', children={'widgets': s1})
    assert PathDispatcher._find(['widgets'], s) == ([], s1)
    with pytest.raises(ValueError):
        PathDispatcher._find(['wodgets'], s)
    s2 = Step('/widgets/*', '*')
    s1 = Step('/widgets', 'widgets', children={'*': s2})
    s = Step('/', 'GET', children={'widgets': s1})
    with pytest.raises(ValueError):
        PathDispatcher._find(['widgets', '1'], s)
    assert PathDispatcher._find(['widgets', '1'], s, wildcard=True) == ([], s2)


def test_pathdispatcher_insert():
    s = Step('/', '/')
    PathDispatcher._insert('/widgets/*/gidgets', ['GET', 'widgets', '*', 'gidgets'],
                           RestFunction('x', '/widgets/<int:foo>/gidgets', 'x'), s)
    assert 'GET' in s
    assert 'widgets' in s.children['GET']
    with pytest.raises(ValueError):
        PathDispatcher._insert('/widgets/*/gidgets', ['GET', 'widgets', '*', 'gidgets'],
                               RestFunction('x', '/widgets/<int:foo>/gidgets', 'x'), s)


def test_pathdispatcher_path_to_parts():
    assert PathDispatcher.path_to_parts('', 'GET') == ['GET', '']
    assert PathDispatcher.path_to_parts('/', 'GET') == ['GET', '']
    assert PathDispatcher.path_to_parts('/foo', 'GET') == ['GET', 'foo']
    assert PathDispatcher.path_to_parts('/foo/bar', 'GET') == ['GET', 'foo', 'bar']
    assert PathDispatcher.path_to_parts('/foo/*/bar', 'GET') == ['GET', 'foo', '*', 'bar']


def test_pathdispatcher_register_rest_function():
    rf = RestFunction('x', '/widgets/<int:foo>/gidgets', 'x')
    p = PathDispatcher()
    p.register_rest_function(rf)
    assert 'x' in p.registry
    assert 'widgets' in p.registry.children['x']
