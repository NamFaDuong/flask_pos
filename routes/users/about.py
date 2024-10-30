from app import app, render_template


@app.route('/about')
def about():  # put application's code here
    return render_template('about.html')
