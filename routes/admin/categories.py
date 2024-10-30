from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/products/categories')
def categories():
    mod = {
        'Products': 'Products',
        'Categories': 'Categories'
    }
    return render_template('admin/categories.html', module=mod)


@app.get('/getCategory')
def category_information():
    data = getcategory()
    return data


@app.post('/delete_category')
def delete_category():
    data = request.get_json()
    category_id = data.get('category_id')
    result = connection.execute(text(f'Delete from categories where id = {category_id}'))
    connection.commit()
    return f"{category_id}"



@app.post('/create_category')
def create_category():
    data = request.get_json()
    name = data['name']
    description = data['description']
    result = connection.execute(text(f"INSERT INTO `categories` VALUES(NULL, '{name}', '{description}');"))
    connection.commit()
    return data



@app.put('/update_category')
def update_category():
    data = request.get_json()
    category_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    result = connection.execute(text(f"UPDATE `categories` SET name='{name}', description='{description}' WHERE id = '{category_id}'"))
    connection.commit()
    return data



@app.post('/category_detail')
def category_detail():
    category_id = request.get_json('id')
    result = connection.execute(text(f'Select * from categories where id = {category_id["id"]}'))
    record = result.fetchall()
    data = []
    for category in record:
        data.append(
            {
                'id': category[0],
                'name': category[1],
                'description': category[2],
            }
        )
    connection.commit()
    return data


def getcategory():
    result = connection.execute(text("SELECT * FROM categories order by id asc "))
    record = result.fetchall()
    data = []
    for category in record:
        data.append(
            {
                'id': category[0],
                'name': category[1],
                'description': category[2]
            }
        )
    connection.commit()
    return data