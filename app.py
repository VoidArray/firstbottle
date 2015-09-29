#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import bottle, sys, sqlite3
import hashlib
import logging

from bottle import request, response, run, route, template, error, static_file, get

@route('/ver')
def index():
    return template('Hello ' + sys.version)

@route('/')
@route('/list')
def notesList():
    c.execute("SELECT id, note, private, short FROM notes")
    result = c.fetchall()
    output = template("pagebody", content="showlist", rows=result)
    return output

@route('/edit')
def editNote():
    return editNote("0")


@route('/save', method='GET')
def saveNote(): #сохранение редактированной записи
    note = request.GET.get("note", "").strip()
    private = request.GET.get("private", "").strip()
    savedId = request.GET.get("key").strip()

    if savedId == "0": #если id Не был сохранен, создаем новую заметку
        m = hashlib.md5()
        m.update(note)
        c.execute("INSERT INTO notes(note, private, short) VALUES(?, ?, ?)",
                   (note, private, m.hexdigest()))
        logging.warning('insert! ')
    elif savedId.isdigit() and int(savedId) != 0:  #пересохраняем по id
        c.execute('''UPDATE notes
            SET note = ?, private = ?
            where id = ? ''', (note, private, savedId))
        logging.warning('update by id! ' + str(savedId))
    elif isinstance(savedId, str): #сохраняем по хешу
        c.execute('''UPDATE notes
            SET note = ?, private = ?
            where short = ? ''', (note, private, savedId))
        logging.warning('update by hash! ' + str(savedId))
    conn.commit()

    bottle.redirect("/")
    return

@route('/edit/<id>', method='GET') # <id:re:[0-9]+>
def editNote(id): #генерируем страницу редактирования
    result = ""
    p = 0
    if id.isdigit() and int(id) != 0:  # ищем по id
        logging.warning("gen edit page id " + str(id))
        c.execute("SELECT note, private FROM notes WHERE id = ?", (id,))
        t = c.fetchone()
        if isinstance(t, tuple):
            (result, p) = t
    elif id != "0" and isinstance(id, str):  # ищем по хэшу
        c.execute("SELECT id, note, private FROM notes WHERE short = ?", (id,))
        t = c.fetchone()
        if isinstance(t, tuple):
            (id, result, p) = t
        logging.warning("gen edit page hash " + str(t))
    #else:  # новая заметка по-умолчанию
    return template("pagebody", content="editnote", note=result, id=id, private=p)

@route('/key/', method='GET')
def searchByKey():
    key1 = request.GET.get("key", "").strip()
    logging.warning("search for: " + key1)
    return bottle.redirect("/edit/" + key1)


@route('/demo')
def addDemoNotes():
    c.execute('create table notes(id INTEGER primary key AUTOINCREMENT, note text not null, private bool, short char(10))')
    c.execute('''insert into notes(note, private, short) values('test!!!',0,'abc')''')
    conn.commit()
    return "<p>Demo added into DB</p>"

# Static Routes
@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')

@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')

@get('/<filename:re:.*\.[png|jpg]>')
def stylesheets(filename):
    return static_file(filename, root='static/img')

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'


# Run bottle internal test server when invoked directly ie: non-uxsgi mode
if __name__ == '__main__':
    bottle.run(host='0.0.0.0', port=80, reloader=True, interval=0.5)
# Run bottle in application mode. Required in order to get the application working with uWSGI!
else:
    application = bottle.default_app()
    bottle.debug(True)

logging.basicConfig(filename='log.txt', format=logging.BASIC_FORMAT)

conn = sqlite3.connect('notes.db')
c = conn.cursor()
