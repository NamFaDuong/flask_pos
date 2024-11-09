from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text
from datetime import *
from routes.admin import products_list

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/pos')
def pos():
    return render_template('admin/pos.html')

@app.route("/getProductForsale")
def getProducts():
    data = products_list.getProductForSale()
    return data

@app.get('/getProductByCategory')
def getProductByCategory():
    category_id = request.args.get("category_id")
    data = products_list.getProductByCategory(category_id)
    return data


@app.post('/pos/payment')
def getPay():
    data = request.get_json()
    invoice(data)
    invoice_id = getInvoice_Id()
    invoiceDetail(data, invoice_id)
    update_Stock(data)
    data = products_list.getProductForSale()
    return data


def getInvoice_Id():
    try:
        result = connection.execute(text("SELECT invoice_id from invoice order by invoice_id desc limit 1;"))
        connection.commit()
        record = result.fetchall()
        for product in record:
            data = product[0]
        return data
    except Exception as error:
        return error


def invoice(data):
    try:
        total_price = data["total_price"]
        discount_percent = data["discount_percent"]
        transaction_datetime = datetime.today()
        result = connection.execute(text(f"""
                    INSERT INTO invoice VALUES(NULL,{total_price}, '{transaction_datetime}', {discount_percent} );
                    """))
        connection.commit()
        return result
    except Exception as error:
        return error


def invoiceDetail(data, invoice_id):
    cart_list = data["cart_list"]
    for item in cart_list:
        product_id = item["product_id"]
        qty = item["qty"]
        result = connection.execute(text(f"""
            INSERT INTO invoice_detail VALUES({invoice_id}, {product_id}, {qty})
            """))
        connection.commit()
    return cart_list


def update_Stock(data):
    cart_list = data["cart_list"]
    for item in cart_list:
        product_id = item["product_id"]
        qty = item["qty"]
        result = connection.execute(text(f"""
                UPDATE products SET qty = qty - {qty} WHERE id = {product_id}
                """))
        connection.commit()
    return data
