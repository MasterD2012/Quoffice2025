from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'quoffice_secret'

# DB setup
def init_db():
    with sqlite3.connect('forum.db') as conn:
        c = conn.cursor()
        c.execute('''
        CREATE TABLE IF NOT EXISTS threads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT, title TEXT, content TEXT,
            username TEXT, timestamp TEXT
        )''')
        c.execute('''
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id INTEGER, content TEXT,
            username TEXT, timestamp TEXT
        )''')

init_db()

@app.route('/')
def index():
    with sqlite3.connect('forum.db') as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM threads ORDER BY id DESC")
        threads = c.fetchall()
    return render_template('index.html', threads=threads)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    with sqlite3.connect('forum.db') as conn:
        c = conn.cursor()
        if request.method == 'POST':
            content = request.form['content']
            c.execute("INSERT INTO replies (thread_id, content, username, timestamp) VALUES (?, ?, ?, ?)",
                      (thread_id, content, session.get('username', 'Guest'), datetime.now().isoformat()))
            conn.commit()
        c.execute("SELECT * FROM threads WHERE id=?", (thread_id,))
        thread = c.fetchone()
        c.execute("SELECT * FROM replies WHERE thread_id=?", (thread_id,))
        replies = c.fetchall()
    return render_template('thread.html', thread=thread, replies=replies)

@app.route('/new', methods=['GET', 'POST'])
def new_thread():
    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        content = request.form['content']
        username = session.get('username', 'Guest')
        timestamp = datetime.now().isoformat()
        with sqlite3.connect('forum.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO threads (category, title, content, username, timestamp) VALUES (?, ?, ?, ?, ?)",
                      (category, title, content, username, timestamp))
            conn.commit()
        return redirect(url_for('index'))
    return render_template('new_thread.html')
