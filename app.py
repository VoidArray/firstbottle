#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import bottle, sys, sqlite3
import hashlib
import logging


from bottle import request, response, run, route, template, error

@route('/ver')
def index():
    return template('Hello ' + sys.version)

@route('/')
@route('/list')
def notesList():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("SELECT id, note, private FROM notes")
    result = c.fetchall()
    conn.close()
    output = template("showlist", rows=result)
    output = template("header") + output
    return output

@route('/edit')
def editNote():
    return editNote(0)


@route('/edit/:id', method='GET')
def editNote(id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    #сохранение редактированной записи
    if request.GET.get('save', '').strip():
        note = request.GET.get("note", "").strip()
        private = request.GET.get("private", "").strip()
        savedId = request.GET.get("hash").strip()

        if (savedId != 0 and str(savedId).isdigit()):  #пересохраняем по id
            c.execute('''UPDATE notes
                SET note = '%s', private = '%s'
                where id = '%s' ''' % (note, private, savedId))
            logging.warning('update by id! ' + str(savedId))
        elif isinstance(savedId, str): #сохраняем по хешу
            c.execute('''UPDATE notes
                SET note = '%s', private = '%s'
                where short = '%s''''' % (note, private, savedId))
            logging.warning('update by hash! ' + str(id))
        else:  #если id Не был сохранен, создаем новую заметку
            m = hashlib.md5()
            m.update(note)
            c.execute("INSERT INTO notes(note, private, short) VALUES('%s', '%s', '%s')"
                      % (note, private, m.hexdigest() ))
            logging.warning('insert! ')
        conn.commit()
        conn.close()

        bottle.redirect("/")
        return

    else:  #генерируем страницу редактирования
        logging.warning("gen new edit page " + str(id))
        if int(id) != 0 and str(id).isdigit():  # ищем по id
            c.execute("SELECT note, private FROM notes WHERE id = '%s'" % id)
            (result, p) = c.fetchone()
            output = template("editnote", note=result, id=id, private=p)
        elif id != "0" and isinstance(id, str):  # ищем по хэшу
            c.execute("SELECT note, short, private FROM notes WHERE short = '%s'" % id)
            (result, findedid, p) = c.fetchone()
            output = template("editnote", note=result, id=findedid, private=p)
        else:  # новая заметка
            output = template("editnote", note="", id=0, private=0)

    conn.close()
    output = template("header") + output
    return output

@route('/bykey', method='GET')
def searchByKey(searchkey):
    bottle.abort(404)
    logging.warning("search for: " + str(searchkey))
    key1 = request.GET.get("key", "").strip()

    return editNote(key1)

@route('/demo')
def addDemoNotes():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('create table notes(id INTEGER primary key AUTOINCREMENT, note text not null, private bool, short char(10))')
    c.execute('''insert into notes(note) values('test!!!')''')
    conn.commit()
    conn.close()
    return "<p>Demo added into DB</p>"

@bottle.error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@bottle.error(404)
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

