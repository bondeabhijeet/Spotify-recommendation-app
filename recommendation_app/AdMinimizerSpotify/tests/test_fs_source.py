

import pytest

from abp.filters.sources import FSSource, NotFound


@pytest.fixture
def fssource_dir(tmpdir):
    tmpdir.mkdir('root')
    not_in_source = tmpdir.join('not-in-source.txt')
    not_in_source.write('! secret')
    root = tmpdir.join('root')
    root.mkdir('foo')
    foobar = root.join('foo', 'bar.txt')
    foobar.write('! foo/bar.txt\n! end')
    return str(root)


@pytest.fixture
def fssource(fssource_dir):
    return FSSource(fssource_dir)


def test_read_file(fssource):
    assert list(fssource.get('foo/bar.txt')) == ['! foo/bar.txt', '! end']


def test_escape_source(fssource):
    with pytest.raises(ValueError):
        list(fssource.get('../not-in-source.txt'))


def test_read_missing_file(fssource):
    with pytest.raises(NotFound):
        list(fssource.get('foo/baz.txt'))


def test_fssource_get_err(fssource):
    with pytest.raises(IOError):
        list(fssource.get(''))
