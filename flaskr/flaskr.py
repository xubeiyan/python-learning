# coding: utf-8

# all the imports
import os
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = 'db.db'
DEBUG = True
SECRET_KEY = '\xd1F\x0ciWP\xb9\x95\xfd\xef\x15#\xa1\x97\xd1\xde\xf0\xfe\xda7\xa9\x8a\x19\xdd'
USERNAME = 'test'
PASSWORD = 'test'

# create our little application >_<
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
	'''Conects to the specific database'''
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv
	
def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
	
def get_db():
	'''Opens a new database connection if there is none yet for the
	current application context.
	'''
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
		
	return g.sqlite_db

@app.before_request
def before_request():
		g.db = connect_db()
	
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()
	
@app.route('/')
def show_entries():
	cur = g.db.execute('select title, text from entries order by id desc')
	entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)
	
@app.route('/add', methods = ['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	g.db.execute('insert into entries (title, text) values (?, ?)',
					[request.form['title'], request.form['text']])
	g.db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			flash('You were logged in')
			return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()