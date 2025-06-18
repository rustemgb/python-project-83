import os

from dotenv import load_dotenv
from flask import Flask, flash, render_template, request

from page_analyzer.data_base import save_url, get_db_connection

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/urls", methods=["POST"])
def create_url():
    input_url = request.form.get("url")
    url_id = save_url(input_url)
    flash('Страница успешно добавлена', 'success')
    return render_template('index.html', url_id=url_id)