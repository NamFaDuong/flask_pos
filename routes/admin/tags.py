from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/products/tags')
def tags():
    mod = {
        'Products': 'Products',
        'Tags': 'Tags'
    }
    return render_template('admin/tags.html', module=mod)


@app.get('/getTags')
def tag_information():
    data = getTags()
    return data


@app.post('/delete_tags')
def delete_tags():
    data = request.get_json()
    tag_id = data.get('tag_id')
    result = connection.execute(text(f'Delete from tags where id = {tag_id}'))
    connection.commit()
    return f"{tag_id}"


@app.post('/create_tags')
def create_tags():
    data = request.get_json()
    name = data['name']
    description = data['description']
    result = connection.execute(text(f"INSERT INTO `tags` VALUES(NULL, '{name}', '{description}');"))
    connection.commit()
    return data


@app.put('/update_tags')
def update_tags():
    data = request.get_json()
    tag_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    result = connection.execute(text(f"UPDATE `tags` SET name='{name}', description='{description}' WHERE id = '{tag_id}'"))
    connection.commit()
    return data


def getTags():
    result = connection.execute(text("SELECT * FROM tags order by id asc "))
    record = result.fetchall()
    data = []
    for tags in record:
        data.append(
            {
                'id': tags[0],
                'name': tags[1],
                'description': tags[2]
            }
        )
    connection.commit()
    return data
