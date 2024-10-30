from app import app, render_template


@app.route('/')
@app.route('/home')
def home():
    return render_template('Home.html')
