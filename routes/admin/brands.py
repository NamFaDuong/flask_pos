from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/products/brands')
def brands():
    mod = {
        'Products': 'Products',
        'Brands': 'Brands'
    }
    return render_template('admin/brands.html', module=mod)


@app.get('/getBrands')
def brands_information():
    data = getBrands()
    return data


@app.post('/delete_brands')
def delete_brands():
    data = request.get_json()
    brand_id = data.get('brand_id')
    result = connection.execute(text(f'Delete from brands where id = {brand_id}'))
    connection.commit()
    return f"{brand_id}"



@app.post('/create_brands')
def create_brands():
    data = request.get_json()
    print(data)
    name = data['name']
    description = data['description']
    print(name)
    print(description)
    result = connection.execute(text(f"INSERT INTO `brands` VALUES(NULL, '{name}', '{description}');"))
    connection.commit()
    return data



@app.put('/update_brands')
def update_brands():
    data = request.get_json()
    print(data)
    brand_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    result = connection.execute(text(f"UPDATE `brands` SET name='{name}', description='{description}' WHERE id = '{brand_id}'"))
    connection.commit()
    return data



@app.post('/brands_detail')
def brands_detail():
    brand_id = request.get_json('id')
    result = connection.execute(text(f'Select * from brands where id = {brand_id["id"]}'))
    record = result.fetchall()
    data = []
    for brand in record:
        data.append(
            {
                'id': brand[0],
                'name': brand[1],
                'description': brand[2],
            }
        )
    connection.commit()
    return data


def getBrands():
    result = connection.execute(text("SELECT * FROM brands order by id asc "))
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