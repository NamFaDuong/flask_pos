from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/products/units')
def units():
    mod = {
        'Products': 'Products',
        'Units': 'Units'
    }
    return render_template('admin/units.html', module=mod)


@app.get('/getUnits')
def units_information():
    data = getUnits()
    return data

@app.post('/delete_units')
def delete_units():
    data = request.get_json()
    unit_id = data.get('unit_id')
    result = connection.execute(text(f'Delete from units where id = {unit_id}'))
    connection.commit()
    return f"{unit_id}"


@app.post('/create_units')
def create_units():
    data = request.get_json()
    print(data)
    name = data['name']
    description = data['description']
    print(name)
    print(description)
    result = connection.execute(text(f"INSERT INTO `units` VALUES(NULL, '{name}', '{description}');"))
    connection.commit()
    return data


@app.put('/update_unit')
def update_unit():
    data = request.get_json()
    brand_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    result = connection.execute(text(f"UPDATE `units` SET name='{name}', description='{description}' WHERE id = '{brand_id}'"))
    connection.commit()
    return data


def getUnits():
    result = connection.execute(text("SELECT * FROM units order by id asc "))
    record = result.fetchall()
    data = []
    for units in record:
        data.append(
            {
                'id': units[0],
                'name': units[1],
                'description': units[2]
            }
        )
    connection.commit()
    return data
