import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, flash
from page_analyzer.data_base import save_url


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
    return render_template('index.html', url=url_id)