import click
import sqlite3

from datetime import datetime
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(err=None):

    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as strm:
        db.executescript(strm.read().decode("utf8"))


@click.command('init-db')
def init_db_com():
    # Clear existing data and create new tables
    click.echo("Initializing database")
    init_db()
    
sqlite3.register_converter(
    "timestamp", lambda x: datetime.fromisoformat(x.decode())
)




def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_com)


