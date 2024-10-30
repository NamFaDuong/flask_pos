from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/users')
def users():
    module = "users"
    return render_template('admin/users.html', module=module)


@app.post('/delete_userid')
def delete_userid():
    data = request.get_json()
    user_id = data.get('user_id')
    result = connection.execute(text(f'Delete from users where id = {user_id}'))
    connection.commit()
    return f"{user_id}"


@app.post('/create_user')
def create_user():
    data = request.get_json()
    name = data['name']
    gender = data['gender']
    phone = data['phone']
    email = data['email']
    print(name)
    result = connection.execute(text(f"INSERT INTO `users` VALUES(NULL, '{name}', '{gender}', '{phone}', '{email}')"))
    connection.commit()
    return "Insert Success"


@app.put('/update_user')
def update_user():
    data = request.get_json()
    user_id = data.get('id')
    name = data.get('name')
    gender = data.get('gender')
    phone = data.get('phone')
    email = data.get('email')
    result = connection.execute(text(f"UPDATE `users` SET name='{name}', gender='{gender}',phone='{phone}',email='{email}' WHERE id = '{user_id}'"))
    connection.commit()
    return "Update Successful"


@app.post('/admin/user_detail')
def view_detail():
    user_id = request.get_json('id')
    result = connection.execute(text(f'Select * from users where id = {user_id["id"]}'))
    record = result.fetchall()
    data = []
    for user in record:
        data.append(
            {
                'id': user[0],
                'name': user[1],
                'gender': user[2],
                'phone': user[3],
                'email': user[4]
            }
        )
    connection.commit()
    return data


@app.get('/getuser')
def getuser():
    result = connection.execute(text("Select * from users order by id asc"))
    record = result.fetchall()
    data = []
    for user in record:
        data.append(
            {
                'id': user[0],
                'name': user[1],
                'gender': user[2],
                'phone': user[3],
                'email': user[4]
            }
        )
    connection.commit()
    return data

