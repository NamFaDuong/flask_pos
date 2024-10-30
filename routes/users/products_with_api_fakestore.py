from app import app, render_template, request
import requests
from datetime import date
from helpers import notifycation


@app.route('/products')
def products():
    res = requests.get('https://fakestoreapi.com/products')
    pro = res.json()
    return render_template('product.html', pro_list=pro)


@app.get('/detail')
def detail():
    id = request.args.get('id')
    res_pro = requests.get(f"https://fakestoreapi.com/products/{id}")
    pro = res_pro.json()
    return render_template('product_detail.html', product = pro)



@app.get('/order')
def order():
    id = request.args.get('id')
    qty = request.args.get('qty')
    pro_infor = requests.get(f"https://fakestoreapi.com/products/{id}")
    pro = pro_infor.json()
    return render_template('product_order.html', product=pro, qty=qty)


@app.post('/confirm')
def confirm():
    pro_id = request.form.get('pro_id')
    pro_qty = request.form.get('pro_qty')
    pro_infor = requests.get(f"https://fakestoreapi.com/products/{pro_id}")
    product = pro_infor.json()
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    address = request.form.get('address')
    html = (
        "<strong>🔔New Confirm information🔔</strong>\n"
        "<strong>Customer\t:  {name}</strong>\n"
        "<strong>Email\t\t:   {email}</strong>\n"
        "<strong>Phone\t\t:   {phone}</strong>\n"
        "<strong>Address\t\t:   {address}</strong>\n"
        "----------------------------------\n"        
        "<strong>Product information</strong>\n"
        "<strong>Product ID : {pro_id}  </strong>\n"
        "<strong>Product Name : {product_name} </strong>\n"
        "<strong>QTY: 1 </strong>\n"
        "<strong>Price : {price} $</strong>\n"
        "<strong>Category : {category} </strong>\n"
        "----------------------------------\n" 
        "<strong>Order Date 📅: {dates}</strong>\n"
    ).format(
        name=name,
        email=email,
        phone=phone,
        address=address,
        dates=date.today(),
        pro_id=pro_id,
        product_name=product['title'],
        price=product['price'],
        category=product['category']
    )
    res = notifycation.sendNotifycation(html)
    if res == 200:
        return render_template('Sending_Successful.html')
    else:
        return render_template('Sending_false.html')
