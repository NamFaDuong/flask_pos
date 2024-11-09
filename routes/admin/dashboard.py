from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text
engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()

@app.route('/admin/dashboard')
@app.route('/admin')
def dashboard():
    module = "dashboard"
    return render_template('admin/dashboard.html', module=module)


@app.get('/admin/countdata')
def countdata():
    user = countUser()
    income = round(totalIncome(), 2)
    product = totalProduct()
    last_order = lastInvoice()
    return {
        'user': user,
        'income': income,
        'product': product,
        'last_order': last_order
    }


def countUser():
    result = connection.execute(text("""
            SELECT COUNT(id) FROM users;
        """))
    record = result.fetchall()
    data = 0
    for user in record:
        data= user[0]
    connection.commit()
    return data

def totalIncome():
    result = connection.execute(text("""
                SELECT SUM(total_amount) FROM invoice;
            """))
    record = result.fetchall()
    data = 0
    for total in record:
        data = total[0]
    connection.commit()
    return data

def totalProduct():
    result = connection.execute(text("""
                SELECT count(id) FROM products;
            """))
    record = result.fetchall()
    data = 0
    for product in record:
        data = product[0]
    connection.commit()
    return data

def lastInvoice():
    result = connection.execute(text("""
                    SELECT invoice.invoice_id, products.`name`,categories.`name` AS category, invoice.transaction_datetime FROM 
                    invoice INNER JOIN invoice_detail ON invoice.invoice_id = invoice_detail.invoice_id 
                    INNER JOIN products ON invoice_detail.product_id = products.id
                    INNER JOIN categories ON products.category_id = categories.id
                    ORDER BY invoice.invoice_id DESC LIMIT 5
                """))
    record = result.fetchall()
    data = []
    for invoice in record:
        data.append(
            {
                'invoice_id': invoice[0],
                'product': invoice[1],
                'category': invoice[2],
                'date': invoice[3],
            }
        )
    connection.commit()
    return data