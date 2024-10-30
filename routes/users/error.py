from app import app, render_template, request


@app.errorhandler(404)
def error404(error):
    return render_template('./error/404.html')


@app.errorhandler(500)
def error404(error):
    return render_template('./error/500.html')
