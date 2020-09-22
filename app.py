from flask import Flask, render_template, url_for, redirect, request, session, flash, get_flashed_messages, abort
from sqlalchemy import create_engine, MetaData
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

db = SQLAlchemy()

# class DBA:
#     self.
#     def __init__():
#         pass


app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
session_variables = []
role = 'farm_guest:guest'


def execute_query(user, password, query):
    conn = psycopg2.connect(
        host="127.0.0.1",
        database="farm",
        user=user,
        password=password
    )
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()


def loadSession(role):
    engine = create_engine(
        f'postgres+psycopg2://{role}@localhost:5432/farm', convert_unicode=True)
    #metadata = MetaData()
    db_session = scoped_session(sessionmaker(
        autocommit=False,  autoflush=False, bind=engine))
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


# --------------404 PAGE------------------
@app.errorhandler(404)
def pageNotFound(error):
    return "<h1>You got 404 mistake please get on correct url adres</h1>"
# ---------------------------------------

# ------------------------LOGIN----------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    global role
    if 'login' and 'username' in session:
        if session['login'] == 'staff':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'farm_staff'
            role = 'farm_staff:staff'
            return redirect(url_for('admin', username=session['username']))
        elif session['login'] == 'director':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'farm_director'
            role = 'farm_director:director'
            return redirect(url_for('director', username=session['username']))
        elif session['login'] == 'farm_client':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'farm_client'
            role = 'farm_client:client'
            return redirect(url_for('trainer', username=session['username']))

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        session_ = loadSession('farm_guest:guest')
        query = f"SELECT role FROM users WHERE login = '{username}' AND password = '{password}' ;"
        print(query)
        try:
            role_ = session_.execute(query).fetchone()[0]
        except Exception as e:
            shutdown_session()
            flash("Неверный логин или пароль")
            return render_template('Registation.html')
            # return f"{e}"

        if session['login'] == 'staff':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'staff'
            role = 'farm_staff:staff'
            return redirect(url_for('admin', username=session['username']))
        elif session['login'] == 'director':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'farm_director'
            role = 'farm_director:director'
            return redirect(url_for('director', username=session['username']))
        elif session['login'] == 'client':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'farm_client'
            role = 'farm_client:client'
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

# -------------------------------------------------------------------


# --------------------------DIRECTOR PAGES---------------------------
@app.route('/director/<username>', methods=['GET'])
def director(username):
    global role
    if 'username' not in session or session['username'] != username:
        abort(401)
    role = "director:123"
    session_ = loadSession(role)
    data1 = session_.execute(
        "SELECT * from staff WHERE position_staff='Директор';")
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
            # return render_template('Add_Staff.html')
            return render_template("Add_Staff.html", username=session['username'])

    else:
        return render_template("Add_Staff.html", username=session['username'])


@app.route('/director/update_staff/<username>', methods=['POST', 'GET'])
def directorupdatestaff(username):
    # fix render template!!
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
            # return render_template('Add_Staff.html')
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


@app.route('/director/check_clients/<username>', methods=('POST', 'GET'))
def director_check_clients(username):
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

@app.route('/director/check_products/<username>', methods=('POST', 'GET'))
def director_check_products(username):
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

@app.route('/director/staff_activity/<username>', methods=('POST', 'GET'))
def director_staff_activity(username):
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

@app.route('/director/subdiv_activity/<username>', methods=('POST', 'GET'))
def director_subdiv_activity(username):
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


@app.route('/director/addsubdiv/<username>', methods=['POST', 'GET'])
def directoraddsubdiv(username):
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
            # return render_template('Add_Staff.html')
            return render_template("Add_Staff.html", username=session['username'])

    else:
        return render_template("Add_Staff.html", username=session['username'])

@app.route('/director/updatesubdiv/<username>', methods=['POST', 'GET'])
def directorupdatesubdiv(username):
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
            # return render_template('Add_Staff.html')
            return render_template("Add_Staff.html", username=session['username'])

    else:
        return render_template("Add_Staff.html", username=session['username'])

@app.route('/director/deletesubdiv/<username>', methods=['POST', 'GET'])
def directordeletesubdiv(username):
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
            # return render_template('Add_Staff.html')
            return render_template("Add_Staff.html", username=session['username'])

    else:
        return render_template("Add_Staff.html", username=session['username'])


@app.route('/director/updatesalary/<username>', methods=['POST', 'GET'])
def directorupdatesalary(username):
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
            # return render_template('Add_Staff.html')
            return render_template("Add_Staff.html", username=session['username'])

    else:
        return render_template("Add_Staff.html", username=session['username'])


# -------------------------------------------------------------------

# --------------------------CLIENT PAGES-----------------------------
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
# client_id = {} and
    if request.method == 'POST':
        first_date = request.form['first_date']
        last_date = request.form['last_date']
        session_ = loadSession('client:client')
        query = f"""SELECT product_id, product_name, product_type, subdivision_id, 
                            product.product_price, quanity_of_produced
                        from client
                            JOIN order_ USING(client_id)
                            JOIN supply USING(order_id)
                            JOIN product USING(product_id)
                            JOIN subdivision USING(subdivision_id)
                            WHERE  order_.date_ between '{first_date}' and '{last_date}';"""
        data = session_.execute(query).all()
        try:
            execute_query('client', 'client', query)
        except Exception as identifier:
            pass
        return render_template('payments.html', data=data, username=session['username'])

    return render_template('payments.html', username=session['username'])


@app.route('/client/check_places/<username>/<city>/', methods=('POST', 'GET'))
def check_places(username, city):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        city = request.form['city']
        session_ = loadSession('client:client')
        query = f"""SELECT subdivision_id, addres, chief_first_name || ' ' || chief_last_name as chief from subdivision
                        where city = '{city}'"""
        try:
            execute_query('client', 'client', query)
        except Exception as identifier:
            pass
    return render_template('city.html', city=city)


@app.route('/client/check_cost/<username>/<product_name>/', methods=('POST', 'GET'))
def check_cost(username, product_name):
    if 'username' not in session or session['username'] != username:
        abort(401)

    session_ = loadSession('client:client')

    if request.method == 'POST':
        product_name = request.form['product_name']

        try:
            data = session_.execute(
                f"""SELECT product_price, quanity_of_produced from product
                        JOIN subdivision USING (subdivision_id)
                        WHERE product_name = '{product_name}'""")
        except Exception as identifier:
            pass
    return render_template('cost.html', data=data, username=session['username'])

# -------------------------------------------------------------------

# --------------------------STAFF PAGES------------------------------
@app.route('/staff/<username>')
def admin(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    session_ = loadSession('admin:admin')
    data1 = session_.execute(f"SELECT * from staff WHERE login='{username}';")
    data1 = data1.first()
    return render_template('Admin.html', dirstaff=data1, username=session['username'])


@app.route('/staff/addclient/<username>', methods=['POST', 'GET'])
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


# -------------------------------------------------------------------

# --------------------------BASE PAGES-------------------------------
@app.route('/home')
@app.route('/')
def home():
    return render_template('farm_main.html')


if __name__ == "__main__":
    app.run(debug=True)
