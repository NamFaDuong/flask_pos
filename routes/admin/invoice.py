from app import app, render_template, request, redirect
from sqlalchemy import create_engine, text

engine = create_engine("mysql+mysqlconnector://root:@127.0.0.1/st89_pos_new")
connection = engine.connect()


@app.route('/admin/invoice')
def invoice():
    module = "invoice"
    return render_template('admin/invoice.html', module=module)

@app.route('/admin/invoice/getAllInvoice')
def getAllInvoice():
    result = connection.execute(text("SELECT * FROM invoice order by invoice_id desc"))
    record = result.fetchall()
    data = []
    for invoice in record:
        data.append(
            {
                'invoice_id': invoice[0],
                'total_amount': invoice[1],
                'transaction_datetime': invoice[2],
                'discount': invoice[3]
            }
        )
    connection.commit()
    return data


@app.get('/admin/invoice/getInvoiceDetail')
def getInvoiceDetail():
    invoice_id = request.args.get("id")
    result = connection.execute(text(f"""
        SELECT invoice_detail.invoice_id,invoice_detail.product_id , products.`name`, invoice_detail.qty FROM invoice_detail 
        INNER JOIN products ON invoice_detail.product_id = products.id
        where invoice_id = {invoice_id};
    """))
    record = result.fetchall()
    data = []
    for invoice in record:
        data.append(
            {
                'invoice_id': invoice[0],
                'product_id': invoice[1],
                'product_name': invoice[2],
                'order_qty': invoice[3],
            }
        )
    connection.commit()
    return data


@app.get('/admin/invoice/getFilter_invoice_id')
def getFilter_invoice_id():
    invoice_id = request.args.get("invoice_id")
    print(invoice_id)
    result = connection.execute(text(f"SELECT * FROM invoice where invoice_id like '{invoice_id}%'"))
    record = result.fetchall()
    print(record)
    data = []
    for invoice in record:
        data.append(
            {
                'invoice_id': invoice[0],
                'total_amount': invoice[1],
                'transaction_datetime': invoice[2],
                'discount': invoice[3]
            }
        )
    connection.commit()
    return data
