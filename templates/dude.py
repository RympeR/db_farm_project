
content = """
    {% extends 'basics.html' %}

    {% block style %}
    <link rel = "stylesheet" href = "{{ url_for('static',filename='css/Delete_Service.css') }}">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet">
    {% endblock %}
{% block title %}Statistics    {% endblock %}
{% block body %}
    <div class = "intro">
        <h1>Посмотреть стоимость</h1>
<div class = "container">
    <img src = "{{ url_for('static',filename='imgs/Service.jpg') }}">
    <form method="post">
        <div class = "dws-input">
        <input type = "text" name = "name" placeholder = "Название услуги:">
        </div>
        <button class = "dws-submit2" type = "submit" name = "submit" value = "Report">Обновить список услуг</button>
        <br />
        <br />
        <br />
        <a class = "restore" href = "/client/{{username}}">Назад</a>
    </form>
</div>
</div>    {% endblock %}
"""

names = [
    'update_staff.html',
    'check_clients.html',
    'check_products.html',
    'check_products_spent.html',
    'staff_activity.html',
    'subdiv_activity.html',
    'addsubdiv.html',
    'updatesubdiv.html',
    'deletesubdiv.html',
    'updatesalary.html',
    'payments.html',
    'city.html',
    'updateclient.html',
    'checkproduct.html',
    'checkclient.html',
    'sold_product.html'
]

for name in names:
    with open(name, 'w') as f:
        f.writelines(content)