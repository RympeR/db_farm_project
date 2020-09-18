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


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    try:
        shutdown_session()
    except Exception as e:
        pass
    try:
        del session['login']
    except Exception as e:
        pass
    try:
        del session['username']
    except Exception as e:
        pass
    print(session)
    return redirect(url_for('login'))

#-------------------------------------------------------------------



#--------------------------DIRECTOR PAGES---------------------------
@app.route('/director/<username>', methods=['GET'])
def director(username):
    global role
    if 'username' not in session or session['username'] != username:
        abort(401)
    role = "director:123"
    session_ = loadSession(role)
    data1 = session_.execute("SELECT * from staff WHERE position_staff='Директор';")
    data1 = data1.first()
    return render_template('Director.html', dirstaff=data1, username=session['username'])


@app.route('/director/addstaff/<username>', methods=['POST', 'GET'])
def directoraddstaff(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    try:
        shutdown_session()
    except Exception as e:
        pass
    if request.method == 'POST':
        username = request.form["name_login"]
        surname = request.form['surname']
        lastname = request.form['patronomyc']
        telephone = request.form['telephone']
        position = request.form["position"]
        service = request.form["service"]
        service_type = request.form["service_type"]
        login_ = request.form["login"]
        password = request.form["passw"]

        session_ = loadSession('director:123')
        query = f"""select * from addnewstaff(
                '{username}', '{surname}', 
                '{lastname}', '{telephone}',
                '{login_}', '{password}',
                '{service}', '{service_type}',
                '{position}');"""

        try:
            execute_query('director', '123', query)
            return redirect(url_for('directoraddstaffres', username=session['username']))
        except Exception as e:
            #return render_template('Add_Staff.html')
            return render_template("Add_Staff.html", username=session['username'])

    else:
        return render_template("Add_Staff.html", username=session['username'])

@app.route('/director/addstaff_result/<username>', methods=['POST', 'GET'])
def directoraddstaffres(username):
    global role
    role = "director:123"
    if 'username' not in session or session['username'] != username:
        abort(401)
    else:
        print(role)
        session_ = loadSession(role)
        data_staff_res = session_.execute("""select name_staff, surname_staff, patronomyc_staff, mobile_telephone_staff,
                                array_agg(coalesce(specialization_service, '')), array_agg(coalesce(type_service, '')),
                                            role_name from staff
                                    full join service on id_service = service_id
                                    full join roles on role_to_login = id_role
                                    group by 1, 2, 3, 4, 7; """)
        data = data_staff_res.fetchall()
        return render_template("Add_Staff2.html", username=session['username'], data=data)


@app.route('/director/delete/<username>', methods=('POST', 'GET'))
def directordelete(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['patronomyc']

        #session_ = loadSession('director:123')
        query = f"""select * from deletestaff(
            '{name}', '{surname}', '{lastname}');"""
        try:
            execute_query('director', '123', query)
            return redirect(url_for('directoraddstaffres', username=session['username']))
        except Exception as e:
            shutdown_session()
            return render_template("Delete.html", username=session['username'])

    return render_template("Delete.html", username=session['username'])

#-------------------------------------------------------------------

#--------------------------CLIENT PAGES-----------------------------
@app.route('/client/<username>')
def client(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    session_ = loadSession('client:client')
    data1 = session_.execute(f"SELECT * from staff WHERE login='{username}';")
    data1 = data1.first()
    return render_template('client_func.html', dirstaff=data1, username=session['username'])

@app.route('/client/check_payment/<username>/<first_date>/<last_date>/', methods=('POST', 'GET'))
def client_check_payment(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        first_date = request.form['first_date']
        last_date = request.form['last_date']

        query = f"""select * from func_name('{first_date}', '{last_date}');"""
        try:
            execute_query('client', 'client', query)
        except Exception as identifier:
            pass
#-------------------------------------------------------------------

#--------------------------STAFF PAGES------------------------------
@app.route('/admin/<username>')
def admin(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    session_ = loadSession('admin:admin')
    data1 = session_.execute(f"SELECT * from staff WHERE login='{username}';")
    data1 = data1.first()
    return render_template('Admin.html', dirstaff=data1, username=session['username'])

@app.route('/admin/newclient/<username>', methods=['POST', 'GET'])
def adminnewclient(username):
    validated = False
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        # shutdown_session()
        # session_ = loadSession('admin:admin')
        phone = request.form['telephone']
        name = request.form['name']
        months = request.form['months']
        try:
            query = f"SELECT * FROM recab('{phone}', '{name}', {months});"
            execute_query('admin', 'admin', query)
            # data = session_.execute()
            # session_.commit()
            validated = True
            return redirect(url_for('admin', username=session['username']))
        except Exception as e:
            return render_template("NewClient.html", username=session['username'])
    return render_template("NewClient.html", username=session['username'])


@app.route('/admin/addclient/<username>', methods=['POST', 'GET'])
def adminaddnewclient(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        lastname = request.form['lastname']
        phone = request.form['telephone']
        try:
            query = f"SELECT * FROM addnewclient('{name}', '{surname}', '{lastname}', '{phone}');"
            execute_query('admin', 'admin', query)
            return redirect(url_for('admin', username=session['username']))
        except Exception as e:
            return render_template("Add_Client.html", username=session['username'])
    return render_template("Add_Client.html", username=session['username'])


#-------------------------------------------------------------------

#--------------------------BASE PAGES-------------------------------
@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
