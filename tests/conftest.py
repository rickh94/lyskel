"""Global pytest fixtures."""
import pytest
import shutil
from pathlib import Path
from tinydb import TinyDB


here = Path(__file__)
basedir = here.parents[1]
srcdir = Path(basedir, 'lyskel')


@pytest.fixture(scope='module')
def livedb(tmpdir_factory):
    """A live database with data."""
    tmpdir_ = tmpdir_factory.mktemp('livedb')
    shutil.copy2(Path(srcdir, 'default_db.json'), Path(tmpdir_))
    return TinyDB(Path(tmpdir_, 'default_db.json'))


@pytest.fixture
def mockdb(monkeypatch, tmpdir):
    """Returns a monkeypatched db."""
    test_db = TinyDB(Path(tmpdir, 'mockdb.json'))

    def mocktables():
        return {'instruments', '_default', 'ensembles'}

    monkeypatch.setattr(test_db, 'tables', mocktables)
    yield test_db
