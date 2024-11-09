from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text
from routes.admin import brands
from routes.admin import categories
from routes.admin import tags
from routes.admin import units

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/products/products_list')
def products_list():
    mod = {
        'Products': 'Products',
        'products_list': 'products_list'
    }
    return render_template('admin/products_list.html', module=mod)


@app.route('/getProduct')
def products_information():
    products_list = getProduct()
    brands_list = brands.getBrands()
    categories_list = categories.getcategory()
    tags_list = tags.getTags()
    units_list = units.getUnits()

    return {
        'products_list': products_list,
        'brands_list': brands_list,
        'categories_list': categories_list,
        'tags_list': tags_list,
        'units_list': units_list,
    }

@app.post("/delete_product")
def delete_product():
    data = request.get_json()
    product_id = data.get('product_id')
    result = connection.execute(text(f'Delete from products where id = {product_id}'))
    connection.commit()
    return f"{product_id}"


@app.post('/new_product')
def new_product():
    data = request.get_json()
    name = data['name']
    description = data['description']
    cost = data['cost']
    price = data['price']
    tag_id = data['tag']
    brand_id = data['brand']
    category = data['category']
    unit_id = data['unit']
    qty = data['qty']
    result = connection.execute(text(f"""
    INSERT INTO products VALUES(
    NULL,'{name}', '{description}',{cost},{price},{category},{unit_id},{brand_id},{tag_id},{qty}
    )
    """))
    connection.commit()
    print(data)
    return data



@app.put("/update_product")
def update_product():
    data = request.get_json()
    product_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    cost = data.get('cost')
    price = data.get('price')
    tag = data.get('tag')
    brand = data.get('brand')
    category = data.get('category')
    unit = data.get('unit')
    result = connection.execute(text(f"""
    UPDATE products 
    SET `name` = '{name}',
        description = '{description}',
        cost = {cost},
        price = {price},
        category_id = {category},
        unit_id = {unit},
        brand_id = {brand},
        tag_id = {tag}
    WHERE id = {product_id}
    """))
    connection.commit()
    return data


@app.get("/products_detail")
def products_detail():
    product_id = request.args.get("id")
    result = connection.execute(text(f"""
            SELECT
            products.id,
            products.name,
            products.description,
            products.cost,
            products.price,
            categories.name AS category_name,
            brands.name AS brand_name,
            units.name AS unit_name,
            tags.name AS tag_name
            FROM
            products
            INNER JOIN categories ON products.category_id = categories.id
            INNER JOIN brands ON products.brand_id = brands.id
            INNER JOIN units ON products.unit_id = units.id
            INNER JOIN tags ON products.tag_id = tags.id
            where products.id = {product_id}
        """))
    record = result.fetchall()
    data = []
    for product in record:
        data.append(
            {
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'cost': product[3],
                'price': product[4],
                'category_name': product[5],
                'brand_name': product[6],
                'unit_name': product[7],
                'tag_name': product[8]
            }
        )
    connection.commit()
    return data


def getProduct():
    result = connection.execute(text("""
        SELECT
        products.id,
        products.name,
        products.description,
        products.cost,
        products.price,
        categories.name AS category_name,
        brands.name AS brand_name,
        units.name AS unit_name,
        tags.name AS tag_name,
        category_id,
        brand_id,
        unit_id,
        tag_id
        FROM
        products
        INNER JOIN categories ON products.category_id = categories.id
        INNER JOIN brands ON products.brand_id = brands.id
        INNER JOIN units ON products.unit_id = units.id
        INNER JOIN tags ON products.tag_id = tags.id;
    """))
    record = result.fetchall()
    data = []
    for product in record:
        data.append(
            {
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'cost': product[3],
                'price': product[4],
                'category_name': product[5],
                'brand_name': product[6],
                'unit_name': product[7],
                'tag_name': product[8],
                'category_id': product[9],
                'brand_id': product[10],
                'unit_id': product[11],
                'tag_id': product[12]
            }
        )
    connection.commit()
    return data



def getProductForSale():
    result = connection.execute(text("""
        SELECT id,name,price,qty FROM products where qty > 0;
    """))
    record = result.fetchall()
    data = []
    for product in record:
        data.append(
            {
                'id': product[0],
                'name': product[1],
                'price': product[2],
                'qty': product[3],
            }
        )
    connection.commit()
    return data


def getProductByCategory(category_id):
    result = connection.execute(text(f"""
            SELECT
            products.id,
            products.name,
            products.description,
            products.cost,
            products.price
            FROM
            products
            WHERE  category_id = {category_id}
        """))
    record = result.fetchall()
    data = []
    for product in record:
        data.append(
            {
                'id': product[0],
                'name': product[1],
                'description': product[2],
                'cost': product[3],
                'price': product[4]
            }
        )
    connection.commit()
    return data