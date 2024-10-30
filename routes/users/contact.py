from app import app, render_template, request
from datetime import date
from helpers import notifycation


@app.route('/contact')
def contact():  # put application's code here
    return render_template('contact.html')


@app.post('/submit_contact')
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    description = request.form.get('description')
    html = (
        "<strong>Name:  {name}</strong>\n"
        "<strong>Email:   {email}</strong>\n"
        "<strong>Phone:   {phone}</strong>\n"
        "<strong>Description:   {description}</strong>\n"
        "----------------------------------\n"
        "<strong>Date:📅  {dates}</strong>\n"
    ).format(
        name=name,
        email=email,
        phone=phone,
        description=description,
        dates=date.today()
    )

    res = notifycation.sendNotifycation(html)
    if res == 200:
        return render_template('contact.html')
    else:
        return render_template('Sending_false.html')
