import click
from flask import current_app, g, jsonify
from flask.cli import with_appcontext
import json

import sqlite3

def convert_row(row):
    lecturer={}
    lecturer["UUID"]=row["UUID"]
    lecturer["title_before"]=row["title_before"]
    lecturer["first_name"]=row["first_name"]
    lecturer["middle_name"]=row["middle_name"]
    lecturer["last_name"]=row["last_name"]
    lecturer["title_after"]=row["title_after"]
    lecturer["picture_url"]=row["picture_url"]
    lecturer["location"]=row["location"]
    lecturer["claim"]=row["claim"]
    lecturer["bio"]=row["bio"]
    lecturer["tags"]=(row["tags"])
    lecturer["price_per_hour"]=row["price_per_hour"]
    lecturer["contact"]=(row["contact"])


    return json.dumps(lecturer)
    # return lecturer





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
    status=post_lecturer({"UUID": "67fda282-2bca-41ef-9caf-039cc5c8dd69","title_before": "Mgr.","first_name": "Petra","middle_name": "Swil","last_name": "Plachá","title_after": "MBA","picture_url": "https://tourdeapp.cz/storage/images/2023_02_25/412ff296a291f021bbb6de10e8d0b94863fa89308843b/big.png.webp","location": "Brno","claim": "Aktivní studentka / Předsedkyně spolku / Projektová manažerka","bio": "<p>Baví mě organizovat věci. Ať už to bylo vyvíjení mobilních aplikací ve Futured, pořádání konferencí, spolupráce na soutěžích Prezentiáda, pIšQworky, <b>Tour de App</b> a Středoškolák roku, nebo třeba dobrovolnictví, vždycky jsem skončila u projektového managementu, rozvíjení soft-skills a vzdělávání. U studentských projektů a akcí jsem si vyzkoušela snad všechno od marketingu po logistiku a moc ráda to předám dál. Momentálně studuji Pdf MUNI a FF MUNI v Brně.</p>","tags": [{"uuid": "6d348a49-d16f-4524-86ac-132dd829b429","name": "Dobrovolnictví"},{"uuid": "8e0568c3-e235-42aa-9eaa-713a2545ff5b","name": "Studentské spolky"},{"uuid": "996c16c8-4715-4de6-9dd0-ea010b3f64c7","name": "Efektivní učení"},{"uuid": "c20b98dd-f37e-4fa7-aac1-73300abf086e","name": "Prezentační dovednosti"},{"uuid": "824cfe88-8a70-4ffb-bcb8-d45670226207","name": "Marketing pro neziskové studentské projekty"},{"uuid": "fa23bea1-489f-4cb2-b64c-7b3cd7079951","name": "Mimoškolní aktivity"},{"uuid": "8325cacc-1a1f-4233-845e-f24acfd0287b","name": "Projektový management, event management"},{"uuid": "ba65a665-e141-40ab-bbd2-f4b1f2b01e42","name": "Fundraising pro neziskové studentské projekty"}],"price_per_hour": 1200,"contact": {"telephone_numbers": ["+420 722 482 974"],"emails": ["placha@scg.cz", "predseda@scg.cz"]}})
    print(status)


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
        return []

def get_lecturer(uuid):
    try:
        db=get_db()
        cur=db.cursor()
        cur.execute("SELECT * FROM record WHERE UUID = ?",(uuid,))
        rows=cur.fetchone()
    # print(rows)
        lecturer=convert_row(rows)
        return lecturer
    except:
        return []

def delete_lecturer(uuid):
    try:
        db=get_db()
        cur=db.cursor()
        cur.execute("DELETE FROM record WHERE UUID = ?",(uuid,))
        db.commit()
        return "OK"
    except:
        conn.rollback()
        return "ERROR"



def put_lecturer(uuid,lecturer):
    try:
        db=get_db()
        cur=db.cursor()
        cur.execute("UPDATE record SET UUID=?,title_before = ?, first_name = ?, middle_name = ?, last_name = ?, title_after = ?, picture_url = ?, location = ?, claim = ?, bio = ?, tags = ?, price_per_hour = ?, contact = ? WHERE UUID = ?",(lecturer["UUID"],lecturer["title_before"], lecturer["first_name"], lecturer["middle_name"], lecturer["last_name"], lecturer["title_after"], lecturer["picture_url"], lecturer["location"], lecturer["claim"], lecturer["bio"], str(lecturer["tags"]), lecturer["price_per_hour"], str(lecturer["contact"]), lecturer["UUID"]))
    # cur.execute("UPDATE record SET title_before=? WHERE uuid = ?",(lecturer["title_before"],lecturer["uuid"]))
        db.commit()
        return get_lecturer(uuid)
    except:
        return "ERROR"

def post_lecturer(lecturer):
    try:
        db=get_db()
        cur=db.cursor()
        cur.execute("INSERT INTO record  (uuid, title_before, first_name, middle_name, last_name, title_after, picture_url, location, claim, bio, tags, price_per_hour, contact) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (lecturer["UUID"], lecturer["title_before"], lecturer["first_name"], lecturer["middle_name"], lecturer["last_name"], lecturer["title_after"], lecturer["picture_url"], lecturer["location"], lecturer["claim"], lecturer["bio"], str(lecturer["tags"]), lecturer["price_per_hour"], str(lecturer["contact"])))

        # cur.execute("INSERT INTO record (uuid,first_name,last_name,contact) VALUES (?,?,?,?)",(lecturer["uuid"],lecturer["first_name"],lecturer["uuid"],lecturer["first_name"]))
        # (?,?)",(lecturer["uuid"],lecturer["first_name"])
        db.commit()

        return get_lecturer(lecturer["UUID"])
    except:
        return "ERROR"
