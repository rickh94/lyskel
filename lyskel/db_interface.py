"""Methods for dealing with tinydb database."""
from pathlib import Path
import os
import shutil
from tinydb import TinyDB, Query

here = Path(__file__).parents[0]
def_path = Path(os.path.expanduser('~'), '.local', 'lyskel', 'db.json')


def pathify(in_path):
    """
    Normalize paths as Path objects.
    Arguments:
        in_path: a pathlike string or Path object
    """
    return Path(in_path)


def init_db(path=def_path):
    """
    Initializes the database.
    Arguments:
        path: (optional) the path of the database.
    """
    path = pathify(path)
    if not path.parents[0].exists():
        os.makedirs(path.parents[0])
    return TinyDB(path)


def bootstrap_db(path=def_path):
    """
    Bootstraps the database from included defaults.
    Arguments:
        path: (optional) the destination of the database.
    """
    path = pathify(path)
    os.makedirs(path.parents[0], exist_ok=True)
    # grab the included default database
    default = Path(here, 'default_db.json')
    shutil.copy2(default, path)


def explore_db(db):
    """
    Explore what tables are available in the database.
    Arguments:
        db: a TinyDB instance.
    """
    if not isinstance(db, TinyDB):
        raise ValueError("'db' must be a TinyDB instance.")
    tables = db.tables()
    if '_default' in tables:
        tables.remove('_default')
    return list(tables)


def explore_table(table, search=None):
    """
    Explore a table in the database.

    Arguments:
        table: the table to search.
        search: (optional) a tuple of (field, search_term) to search for in the
        table.
    """
    founditems = []
    if search is None:
        items = table.all()
    else:
        if not isinstance(search, tuple):
            raise ValueError('search must be a tuple (field, value)')
        field, term = search
        Search = Query()
        # Search[field]: look specified field, lambda val: return the value
        # from the db if the term is found in it.
        items = table.search(Search[field].test(lambda val: term in val))
    for item in items:
        try:
            founditems.append(item['name'])
        except KeyError:
            pass

    return founditems


def check_table(table, search):
    """
    Check whether something is in a particular table in the database.
    """
    if explore_table(table, search=('name', search)):
        return True
    return False