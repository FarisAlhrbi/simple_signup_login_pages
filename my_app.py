import sqlite3
import bcrypt
from flask import Flask,render_template,request,redirect

app = Flask(__name__)


def init_db():
    db = sqlite3.connect("my_app.db")
    cr = db.cursor()
    cr.execute("create table if not exists users(name String UNIQUE NOT NULL, email String UNIQUE, password String NOT NULL, user_id Integer PRIMARY KEY AUTOINCREMENT)")
    db.commit()
    db.close()

init_db()

@app.route("/")
@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route("/signup", methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        conn = sqlite3.connect("my_app.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",(username, email, hashed_pass))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return "You Have Account Before"
        
    return render_template("signup.html")


@app.route("/login" , methods=['GET',"POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['pass']
        
        conn = sqlite3.connect("my_app.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, email, password, user_id FROM users WHERE name = ? and email = ?",(username, email))
        data = cursor.fetchone()
        if data and bcrypt.checkpw(password.encode('utf-8'), data[2]):
            conn.close()
            return f"مرحبًا {username}! تم تسجيل الدخول بنجاح"
        else:
            conn.close()
            return "اسم المستخدم أو كلمة المرور خاطئة"
    
    return render_template("login.html")


if __name__ == "__main__":
    app.run()