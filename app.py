from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import requests
from datetime import date
from sqlalchemy import create_engine, text

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run()

import routes
