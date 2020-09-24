from flask import Flask, render_template, url_for, redirect, request, session, flash, get_flashed_messages, abort
from model import *

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'
session_variables = []
role = 'farm_guest:guest'



def loadSession(role):
    engine = create_engine(
        f'postgres+psycopg2://{role}@localhost:5432/farm', convert_unicode=True)
    # metadata = MetaData()
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
        elif session['login']:
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['login'] = 'farm_client'
            role = 'farm_client:client'
            return redirect(url_for('client', username=session['username']))

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form['password']
        session_ = loadSession('farm_guest:guest')
        query = f"SELECT role_ FROM staff WHERE login = '{username}' AND passw = '{password}' ;"
        print(query)
        try:
            session['login'] = session_.execute(query).fetchone()[0]
        except Exception as e:

            try:
                query = f"SELECT client_id FROM client WHERE login = '{username}' AND passw = '{password}' ;"
                print(query)
                session['login'] = session_.execute(query).fetchone()[0]
                print(session['login'])
                if session['login'] > 0:
                    session['username'] = username
                    role = 'farm_staff:staff'
                    return redirect(url_for('client', username=session['username']))
            except Exception as e:
                print(e)
                shutdown_session()
                flash("Неверный логин или пароль")
                return render_template('Registation.html')
            # return f"{e}"

        if session['login'] == 'staff':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['username'] = username
            role = 'farm_staff:staff'
            return redirect(url_for('admin', username=session['username']))
        elif session['login'] == 'director':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['username'] = username
            role = 'farm_director:director'
            return redirect(url_for('director', username=session['username']))
        elif session['login'] == 'client':
            try:
                shutdown_session()
            except Exception as e:
                pass
            session['username'] = username
            role = 'farm_client:client'
            return redirect(url_for('client', username=session['username']))
        else:
            flash("Неверный логин или пароль")
            return render_template('Registation.html')

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
    role = "farm_director:director"
    session_ = loadSession(role)
    data1 = session_.execute(
        "SELECT * from staff WHERE role_='director';")
    data1 = data1.first()
    print(data1)
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
        work_role = request.form['work_role']
        telephone = request.form['telephone']
        salary = request.form['salary']
        quantity = request.form['quantity']
        subdivision = request.form['subdivision']
        adres = request.form['adres']
        position = request.form['position']
        login_ = request.form['login']
        password = request.form['password']

        session_ = loadSession('farm_director:director')
        query = f"""            
                INSERT INTO Staff(First_name, Last_name, Phone_number, Work_role, Quantity_of_products_produced,
                    Salary, Subdivision_ID, Adress, cheese_equipment, milk_equipment, login, passw, role_)
                values('{username}','{surname}','{telephone}','{work_role}','{quantity}','{salary}','{subdivision}','{adres}','false','true', '{login_}', '{password}', '{position}');
        """

        try:
            execute_query('farm_director', 'director', query)
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
        staff_id = request.form["staff_id"]
        username = request.form["name_login"]
        surname = request.form['surname']
        work_role = request.form['work_role']
        telephone = request.form['telephone']
        salary = request.form['salary']
        quantity = request.form['quantity']
        subdivision = request.form['subdivision']
        adres = request.form['adres']
        position = request.form['position']
        login_ = request.form['login']
        password = request.form['password']

        session_ = loadSession('farm_director:director')
        query = f'''
            UPDATE staff
            set
                First_name = '{username}',
                Last_name = '{surname}',
                Phone_number = '{telephone}',
                Work_role = '{work_role}',
                Quantity_of_products_produced = '{quantity}',
                Salary = '{salary}',
                Subdivision_ID = '{subdivision}',
                Adress = '{adres}',
                login = '{login_}',
                passw = '{password}',
                role_ = '{position}'
            where staff_id = {staff_id};
        '''
        print(query)

        try:
            execute_query('farm_director', 'director', query)
            return redirect(url_for('directoraddstaffres', username=session['username']))
        except Exception as e:
            return render_template("update_staff.html", username=session['username'])

    else:
        return render_template("update_staff.html", username=session['username'])


@app.route('/director/addstaff_result/<username>', methods=['POST', 'GET'])
def directoraddstaffres(username):
    global role
    role = "farm_director:director"
    if 'username' not in session or session['username'] != username:
        abort(401)
    else:
        query = """select * from staff;"""
        data = execute_select_query('farm_director', 'director', query)
        return render_template("Add_Staff2.html", username=session['username'], data=data)


@app.route('/director/delete/<username>', methods=('POST', 'GET'))
def directordelete(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        number = request.form['number']

        query = f"DELETE from staff where staff_id = {number};"

        try:
            execute_query('farm_director', 'director', query)
            return redirect(url_for('directoraddstaffres', username=session['username']))
        except Exception as e:
            return render_template("Delete.html", username=session['username'])

    return render_template("Delete.html", username=session['username'])


@app.route('/director/check_products_spent/<username>', methods=('POST', 'GET'))
def director_spent_products(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        date_begin = request.form['date_begin']
        date_end = request.form['date_end']

        query = f"select * from sold_product('{date_begin}', '{date_end}');"

        try:
            data = execute_select_query('farm_director', 'director', query)
            return render_template("spent_products.html", username=session['username'], data=data)

        except Exception as e:
            pass
        return render_template("spent_products.html", username=session['username'])
    return render_template("spent_products.html", username=session['username'])


@app.route('/director/check_products/<username>', methods=('POST', 'GET'))
def director_check_products(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        name = request.form['name']

        query = f"select * from check_product('{name}');"

        try:
            data = execute_select_query('farm_director', 'director', query)
            return render_template("check_products.html", username=session['username'], data=data)
        except Exception as e:
            # return render_template('Add_Staff.html')
            return render_template("check_products.html", username=session['username'])
    return render_template("check_products.html", username=session['username'])


@app.route('/director/staff_activity/<username>', methods=('POST', 'GET'))
def director_staff_activity(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        number = request.form['number']

        query = f"""SELECT staff_id, last_name || ' ' || first_name as fio, chief_first_name || ' ' || chief_last_name as chief_fio, quantity_of_products_produced 
                        from staff
                        join subdivision using(subdivision_id)
                        where staff_id = {number};"""

        try:
            data = execute_select_query('farm_director', 'director', query)
            return render_template("staff_activity.html", username=session['username'], data=data)
        except Exception as e:
            pass

    return render_template("staff_activity.html", username=session['username'])


@app.route('/director/subdiv_activity/<username>', methods=('POST', 'GET'))
def director_subdiv_activity(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        adres = request.form['adres']

        query = f"""
            select chief_first_name || ' ' || chief_last_name as chief_fio, product_type, quanity_of_produced, sum(product_count) as sold_amount
                from subdivision
                    join product USING(subdivision_id)
                    join supply USING(product_id)
                where addres = '{adres}'
                GROUP by 1,2,3;
        """

        try:
            data = execute_select_query('farm_director', 'director', query)
            return render_template("subdiv_activity.html", username=session['username'], data=data)
        except Exception as e:
            pass
    return render_template("subdiv_activity.html", username=session['username'])


@app.route('/director/addsubdiv/<username>', methods=['POST', 'GET'])
def directoraddsubdiv(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    try:
        shutdown_session()
    except Exception as e:
        pass
    if request.method == 'POST':
        adres = request.form["adres"]
        city = request.form["city"]
        name = request.form["name"]
        surname = request.form["surname"]
        quantity = request.form["quantity"]

        query = f"""
            INSERT INTO subdivision(chief_first_name, chief_last_name,city, quanity_of_produced, addres) 
                VALUES('{name}', '{surname}', '{city}', {quantity}, '{adres}');
        """

        try:
            execute_query('farm_director', 'director', query)
        except Exception as e:
            pass
        return render_template("addsubdiv.html", username=session['username'])

    else:
        return render_template("addsubdiv.html", username=session['username'])


@app.route('/director/updatesubdiv/<username>', methods=['POST', 'GET'])
def directorupdatesubdiv(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    try:
        shutdown_session()
    except Exception as e:
        pass
    if request.method == 'POST':
        sub_id = request.form["sub_id"]
        adres = request.form["adres"]
        city = request.form["city"]
        name = request.form["name"]
        surname = request.form["surname"]
        quantity = request.form["quantity"]

        query = f'''UPDATE subdivision
                    SET
                        chief_first_name = '{name}',
                        chief_last_name = '{surname}',
                        city = '{city}',
                        quanity_of_produced = '{quantity}',
                        addres = '{adres}'
                    WHERE subdivision_id = {sub_id};'''

        try:
            execute_query('farm_director', 'director', query)
        except Exception as e:
            pass
        return render_template("updatesubdiv.html", username=session['username'])

    else:
        return render_template("updatesubdiv.html", username=session['username'])


@app.route('/director/deletesubdiv/<username>', methods=['POST', 'GET'])
def directordeletesubdiv(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    try:
        shutdown_session()
    except Exception as e:
        pass
    if request.method == 'POST':
        sub_id = request.form["sub_id"]

        query = f"delete from subdivision where subdivision_id = {sub_id};"

        try:
            execute_query('farm_director', 'director', query)
        except Exception as e:
            pass
        return render_template("deletesubdiv.html", username=session['username'])

    else:
        return render_template("deletesubdiv.html", username=session['username'])


@app.route('/director/updatesalary/<username>', methods=['POST', 'GET'])
def directorupdatesalary(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    try:
        shutdown_session()
    except Exception as e:
        pass
    if request.method == 'POST':
        number = request.form["number"]
        salary = request.form['salary']

        query = f"""UPDATE staff
                    set salary = {salary}
                    WHERE staff_id = {number};"""

        try:
            execute_query('farm_director', 'director', query)
        except Exception as e:
            pass
        return render_template("updatesalary.html", username=session['username'])

    else:
        return render_template("updatesalary.html", username=session['username'])


# -------------------------------------------------------------------

# --------------------------CLIENT PAGES-----------------------------
@app.route('/client/<username>')
def client(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    session_ = loadSession('farm_client:client')
    data1 = session_.execute(f"SELECT * from client WHERE login='{username}';")
    data1 = data1.first()
    print(data1)
    return render_template('Client.html', dirstaff=data1, username=session['username'])


@app.route('/client/check_payment/<username>/', methods=('POST', 'GET'))
def client_check_payment(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        first_date = request.form['first_date']
        last_date = request.form['last_date']

        query = f"""select * from client_bought_product('{first_date}', '{last_date}', '{session['username']}');"""
        print(query)
        try:
            data = execute_select_query('farm_client', 'client', query)
            return render_template('payments.html', data=data, username=session['username'])
        except Exception as identifier:
            pass

    return render_template('payments.html', username=session['username'])

@app.route('/client/add_order/<username>/', methods=('POST', 'GET'))
def client_add_order(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        prod_name = request.form['prod_name']
        prod_amount = request.form['prod_amount']

        query = f"""select * from add_order('{prod_name}', {prod_amount}, '{session['username']}');"""
        print(query)
        try:
            data = execute_select_query('farm_client', 'client', query)
            return render_template('add_client_order.html', username=session['username'])
        except Exception as identifier:
            pass

    return render_template('add_client_order.html', username=session['username'])

@app.route('/client/check_places/<username>/', methods=('POST', 'GET'))
def check_places(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        city = request.form['city']
        query = f"""SELECT subdivision_id, addres, chief_first_name || ' ' || chief_last_name as chief from subdivision
                        where city = '{city}'"""
        try:
            data = execute_select_query('farm_client', 'client', query)
            return render_template('city.html', username=session['username'], data=data)
        except Exception as identifier:
            pass
    return render_template('city.html', username=session['username'])


@app.route('/client/check_cost/<username>/', methods=('POST', 'GET'))
def check_cost(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        product_name = request.form['product_name']

        try:
            query = f"""SELECT product_price, quanity_of_produced from product
                        JOIN subdivision USING (subdivision_id)
                        WHERE product_name = '{product_name}';"""
            print(query)
            data = execute_select_query('farm_client', 'client', query)
            return render_template('cost.html', data=data, username=session['username'])
        except Exception as identifier:
            pass
    return render_template('cost.html', username=session['username'])

# -------------------------------------------------------------------

# --------------------------STAFF PAGES------------------------------
@app.route('/admin/<username>')
def admin(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    session_ = loadSession('farm_staff:staff')
    data1 = session_.execute(f"SELECT * from staff  WHERE login='{username}';")
    data1 = data1.first()
    print(data1)
    return render_template('Admin.html', dirstaff=data1, username=session['username'])


@app.route('/admin/check_resources/<username>')
def check_resources(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    data = execute_select_query("farm_staff","staff",f"SELECT * from order_resource;")
    return render_template('check_resources.html', data=data, username=session['username'])


@app.route('/admin/order_resource/<username>/', methods=('POST', 'GET'))
def add_order(username):
    if 'username' not in session or session['username'] != username:
        abort(401)

    if request.method == 'POST':
        type_ = request.form['type']
        price = request.form['price']
        count = request.form['count']
        subdiv = request.form['subdiv']

        query = f"""INSERT INTO order_resource(resource_type, resource_price,
                        resource_count, subdivision_id) VALUES
                    ('{type_}','{price}','{count}',{subdiv});"""
        try:
            print(query)
            execute_query('farm_staff', 'staff', query)
            return render_template('add_resource.html', username=session['username'])
        except Exception as identifier:
            pass
    return render_template('add_resource.html', username=session['username'])


@app.route('/admin/addclient/<username>', methods=['POST', 'GET'])
def adminaddnewclient(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        name = request.form['name']
        adress = request.form['adress']
        surname = request.form['surname']
        phone = request.form['phone']
        login_ = request.form['login_']
        password = request.form['password']
        try:
            query = f"SELECT * FROM insert_new_client('{surname}', '{name}', '{phone}', '{adress}', '{login_}', '{password}' );"
            execute_query('farm_staff', 'staff', query)
            return redirect(url_for('admin', username=session['username']))
        except Exception as e:
            return render_template("Add_Client.html", username=session['username'])
    return render_template("Add_Client.html", username=session['username'])


@app.route('/admin/updateclient/<username>', methods=['POST', 'GET'])
def adminupdateclient(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        phone = request.form['phone']
        adres = request.form['adres']
        try:
            query = f"SELECT * FROM update_client('{name}', '{surname}', '{phone}', '{adres}');"
            execute_query('farm_staff', 'staff', query)
            return redirect(url_for('admin', username=session['username']))
        except Exception as e:
            return render_template("updateclient.html", username=session['username'])
    return render_template("updateclient.html", username=session['username'])


@app.route('/admin/checkproduct/<username>', methods=['POST', 'GET'])
def admincheckproduct(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        product_name = request.form['product_name']

        try:
            query = f"select * from check_product('{product_name}');"
            print(query)
            data = execute_select_query('farm_staff', 'staff', query)
            return render_template("checkproduct.html", username=session['username'], data=data)
        except Exception as e:
            return render_template("checkproduct.html", username=session['username'])
    return render_template("checkproduct.html", username=session['username'])


@app.route('/admin/checkclient/<username>', methods=['POST', 'GET'])
def admincheckclient(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        client_name = request.form['client_name']
        client_sur = request.form['client_sur']

        try:
            query = f"SELECT * from client_info WHERE last_name = '{client_sur}' and first_name = '{client_name}';"
            data = execute_select_query('farm_staff', 'staff', query)
            print(data)
            return render_template("checkclient.html", username=session['username'], data=data)
        except Exception as e:
            return render_template("checkclient.html", username=session['username'])
    return render_template("checkclient.html", username=session['username'])


@app.route('/admin/sold_product/<username>', methods=['POST', 'GET'])
def adminsold_product(username):
    if 'username' not in session or session['username'] != username:
        abort(401)
    if request.method == 'POST':
        date_beg = request.form['date_beg']
        date_end = request.form['date_end']

        try:
            query = f"select * from sold_product('{date_beg}', '{date_end}');"
            print(query)
            data = execute_select_query('farm_staff', 'staff', query)

            return render_template("sold_product.html", username=session['username'], data=data)
        except Exception as e:
            return render_template("sold_product.html", username=session['username'])
    return render_template("sold_product.html", username=session['username'])

# -------------------------------------------------------------------

# --------------------------BASE PAGES-------------------------------
@app.route('/home')
@app.route('/')
def home():
    return render_template('farm_main.html')


if __name__ == "__main__":
    app.run(debug=True)
