from flask import Flask, render_template, url_for,redirect, request, session, flash, get_flashed_messages, abort
from sqlalchemy import create_engine, MetaData
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

db = SQLAlchemy()

# class DBA:
#     self.
#     def __init__():
#         pass


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
session_variables = []
role = 'guest:123456'


conn = psycopg2.connect(
    host = '127.0.0.1',
    user='postgres',
    password='b01210b',
    database='db_farm'
)

def execute_query(user, password, query):
    conn = psycopg2.connect(
                host="127.0.0.1",
                database="Cursovoi_Project",
                user=user,
                password=password
    )
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def loadSession(role):
    engine = create_engine(f'postgres+psycopg2://{role}@localhost:5432/Cursovoi_Project', convert_unicode=True)
    #metadata = MetaData()
    db_session = scoped_session(sessionmaker(autocommit=False,  autoflush=False, bind=engine))
    metadata = db.metadata
    session_variables.append(engine)
    session_variables.append(db_session)
    session_variables.append(metadata)
    Session = sessionmaker(bind=engine)
    session_ = Session()
    return session_


def shutdown_session(exception=None):
    global session_variables
    session_variables[1].remove()



cursor = conn.cursor()
#--------------404 PAGE------------------
@app.errorhandler(404)
def pageNotFound(error):
    return "<h1>You got 404 mistake please get on correct url adres</h1>"
#---------------------------------------

#------------------------LOGIN----------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    global role
    if 'login' and 'username' in session:
        if session['login'] == 'admin':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'admin'
            role = 'admin:admin'
            return redirect(url_for('admin', username=session['username']))
        elif session['login'] =='director':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'director'
            role = 'director:123'
            return redirect(url_for('director', username=session['username']))
        elif session['login'] == 'trainer':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'trainer'
            role = 'trainer:trainer'
            return redirect(url_for('trainer', username=session['username']))

    if request.method == 'POST' :
        username = request.form["username"]
        password = request.form['password']
        session_ = loadSession('guest:123456')
        query = f"SELECT role_name FROM roles JOIN staff ON role_to_login=id_role WHERE login = '{username}' AND passw = '{password}' ;"

        try:
            role_ = session_.execute(query).fetchone()[0]
        except Exception as e:
            shutdown_session()
            flash("Неверный логин или пароль")
            return render_template('Registation.html')
            # return f"{e}"

        if role_ == 'administrator':
            shutdown_session()
            session['login'] = 'admin'
            session['username'] = username
            role = 'admin:admin'
            return redirect(url_for('admin', username=session['username']))
        elif role_ == 'director':
            shutdown_session()
            session['login'] = 'director'
            session['username'] = username
            role='director:123'
            return redirect(url_for('director', username=session['username']))
        elif role_ == 'trainer':
            shutdown_session()
            session['login'] = 'trainer'
            session['username'] = username
            role = 'trainer:trainer'
            return redirect(url_for('trainer', username=session['username']))
        else:
            flash("Неверный логин или пароль")
    return render_template('Registation.html')

#-------------------------------------------------------------------


@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
