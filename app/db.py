import click
from flask import current_app, g
from flask.cli import with_appcontext

import sqlite3

def convert_row(row):
    lecturer={}
    lecturer["uuid"]=row["uuid"]
    lecturer["title_before"]=row["title_before"]
    lecturer["first_name"]=row["first_name"]
    lecturer["middle_name"]=row["middle_name"]
    lecturer["last_name"]=row["last_name"]
    lecturer["title_after"]=row["title_after"]
    lecturer["picture_url"]=row["picture_url"]
    lecturer["location"]=row["location"]
    lecturer["claim"]=row["claim"]
    lecturer["bio"]=row["bio"]
    lecturer["tags"]=row["tags"]
    lecturer["price_per_hour"]=row["price_per_hour"]
    lecturer["contact"]=row["contact"]


    return lecturer





def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Inicializuje databázi dle schema.sql
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))





@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Definujeme příkaz příkazové řádky
    """
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_lecturers():
    try:
        db=get_db()
        cur=db.cursor()
        cur.execute("SELECT * FROM record")
        rows=cur.fetchall()
        lecturers=[]
        for row in rows:
            lecturers.append(convert_row(row))


        return lecturers
    except:
        return "Error getting lecturers"

def get_lecturer(uuid):
    # try:
    db=get_db()
    cur=db.cursor()
    cur.execute("SELECT * FROM record WHERE uuid = ?",(uuid,))
    rows=cur.fetchone()
    # print(rows)
    lecturer=convert_row(rows)
    return lecturer
    # except:
    #     return "Error getting lecturer"

def delete_lecturer(uuid):
    # try:
    db=get_db()
    cur=db.cursor()
    cur.execute("DELETE FROM record WHERE uuid = ?",(uuid,))
    db.commit()
    return "Success"
    # except:
    #     conn.rollback()
    #     return "Error deleting lecturer"



def put_lecturer(uuid,lecturer):
    # try:
    db=get_db()
    cur=db.cursor()
    cur.execute("UPDATE record SET title_before = ?, first_name = ?, middle_name = ?, last_name = ?, title_after = ?, picture_url = ?, location = ?, claim = ?, bio = ?, tags = ?, price_per_hour = ?, contact = ? WHERE uuid = ?",(lecturer["title_before"], lecturer["first_name"], lecturer["middle_name"], lecturer["last_name"], lecturer["title_after"], lecturer["picture_url"], lecturer["location"], lecturer["claim"], lecturer["bio"], lecturer["tags"], lecturer["price_per_hour"], lecturer["contact"], lecturer["uuid"]))
    # cur.execute("UPDATE record SET title_before=? WHERE uuid = ?",(lecturer["title_before"],lecturer["uuid"]))
    db.commit()
    return "Success updating lecturer"
    # except:
    #     return "Error updating lecturer"

def post_lecturer(lecturer):
    # try:
    db=get_db()
    cur=db.cursor()
    cur.execute("INSERT INTO record  (uuid, title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, tags, price_per_hour, contact) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (lecturer["uuid"], lecturer["title_before"], lecturer["first_name"], lecturer["middle_name"], lecturer["last_name"], lecturer["title_after"], lecturer["picture_url"], lecturer["location"], lecturer["claim"], lecturer["bio"], lecturer["tags"], lecturer["price_per_hour"], lecturer["contact"]))

    # cur.execute("INSERT INTO record (uuid,first_name,last_name,contact) VALUES (?,?,?,?)",(lecturer["uuid"],lecturer["first_name"],lecturer["uuid"],lecturer["first_name"]))
    # (?,?)",(lecturer["uuid"],lecturer["first_name"])
    db.commit()

    return "Sucess creating lecturer"
    # except:
    #     return "Error creating lecturer"
