from flask import Flask, Blueprint, render_template, request, redirect, url_for, session
import sqlite3
import os

# Create the Flask app
app = Flask(__name__)
app.secret_key = 'quoffice_secret'

# Define the Blueprint
forum_bp = Blueprint('forum', __name__, url_prefix='/forums', template_folder='templates')

# Set up database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'forum.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT,
                category TEXT,
                author TEXT
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thread_id INTEGER,
                content TEXT,
                author TEXT
            )
        ''')
    print("Database initialized.")

@forum_bp.route('/')
def index():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM threads")
        threads = c.fetchall()
    return render_template('index.html', threads=threads)

@forum_bp.route('/thread/<int:thread_id>', methods=['GET', 'POST'])
def thread(thread_id):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        if request.method == 'POST':
            reply = request.form['reply']
            author = session.get('username', 'Anonymous')
            c.execute("INSERT INTO replies (thread_id, content, author) VALUES (?, ?, ?)", (thread_id, reply, author))
            conn.commit()
        c.execute("SELECT * FROM threads WHERE id=?", (thread_id,))
        thread = c.fetchone()
        c.execute("SELECT * FROM replies WHERE thread_id=?", (thread_id,))
        replies = c.fetchall()
    return render_template('thread.html', thread=thread, replies=replies)

@forum_bp.route('/new', methods=['GET', 'POST'])
def new_thread():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        author = session.get('username', 'Anonymous')
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO threads (title, content, category, author) VALUES (?, ?, ?, ?)", (title, content, category, author))
            conn.commit()
        return redirect(url_for('forum.index'))
    return render_template('new_thread.html')

@forum_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('forum.index'))
    return render_template('login.html')

@forum_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('forum.index'))

# Register the blueprint
app.register_blueprint(forum_bp)

# Initialize the database
init_db()

if __name__ == '__main__':
    app.run(debug=True)
