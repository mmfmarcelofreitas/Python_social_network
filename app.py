from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):  # You'll have to define this function
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')  # Assuming that your login form is in a file called login.html

@app.route('/home', methods=['GET'])
def home():
    posts = get_posts_from_db()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        save_user_to_db(username, email, password)
        return redirect(url_for('home'))
    return render_template('register.html')

@app.route('/post', methods=['POST'])
def post():
    text = request.form['text']
    if len(text) > 240:
        return "A quantidade máxima de carácteres é de 240", 400
    save_to_db(text)
    return redirect(url_for('home'))

@app.route('/delete', methods=['POST'])
def delete():
    post_id = request.form['post_id']
    delete_from_db(post_id)
    return redirect(url_for('home'))

def save_to_db(text):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (text) VALUES (?)", (text,))
    conn.commit()
    conn.close()

def save_user_to_db(username, email, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()

def get_posts_from_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return posts

def delete_from_db(post_id):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute(f"DELETE FROM posts WHERE id = {post_id}")
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # Look for a user with the provided username and password in the database
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()
    conn.close()
    # If such a user is found, return True. Otherwise, return False.
    return user is not None

if __name__ == "__main__":
    app.run(debug=True)