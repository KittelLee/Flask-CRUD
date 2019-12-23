from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tb_post')
    rows = c.fetchall(); 
    return render_template("index.html", posts = rows)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template("create.html")


    elif request.method == "POST":
        result = request
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        Title = request.form['title']
        Contents = request.form['contents']
        Creator = request.form['creator']

        query = 'INSERT INTO tb_post(title, contents, creator) VALUES(?, ?, ?)'
        c.execute(query, (Title, Contents, Creator))
        conn.commit()
        return redirect('/')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "GET":
        result  = request.args['number']
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        query = 'SELECT * from tb_post where number = ?'
        c.execute(query, (result,))
        save = c.fetchone()

        return render_template("update.html", post = save)


    if request.method == "POST":
        result = request
        conn = sqlite3.connect('flask.db')
        c = conn.cursor()
        Number = request.form['number']
        Title = request.form['title']
        Contents = request.form['contents']
        Creator = request.form['creator']

        query = 'UPDATE tb_post SET number = ?, title = ?, contents = ?, creator = ?'
        c.execute(query, (Number, Title, Contents, Creator))
        conn.commit()
        return redirect('/')


@app.route('/delete', methods=['POST'])
def delete():
    delete = request.form['number']
    conn = sqlite3.connect('flask.db')
    c = conn.cursor()
    query = 'DELETE FROM tb_post WHERE number = ?'
    c.execute(query, (delete,))
    conn.commit()
    return redirect('/')


def init_db():
    conn = sqlite3.connect('flask.db')
    cursor = conn.cursor()
    query = '''
        CREATE TABLE IF NOT EXISTS "tb_post" (
            "number"    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            "title"     TEXT NOT NULL,
            "contents"  TEXT NOT NULL,
            "creator"   TEXT NOT NULL
        );
    '''
    cursor.execute(query)
    conn.commit()
    return
    

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)