import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer.data_base import (
    get_db_connection,
    get_existing_urls,
    save_url,
)
from page_analyzer.parser import parse_url
from page_analyzer.url_validator import validate_url

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')


@app.route("/urls", methods=["POST"])
def create_url():
    input_url = request.form.get("url")
    error_message = validate_url(input_url)
    if error_message:
        flash(error_message, "error")
        return render_template("index.html", url=input_url), 422
    base_input_domain = parse_url(input_url)
    existing_urls = get_existing_urls()
    if existing_urls:
        for existing_url in existing_urls:
            if base_input_domain == parse_url(existing_url[1]):
                flash('Страница уже существует', 'error')
                return redirect(url_for('url_detail', url_id=existing_url[0]))
    url_id = save_url(input_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_detail', url_id=url_id))


@app.route("/urls", methods=["GET"])
def all_urls():
    sql = '''
        SELECT urls.id, urls.name, urls.created_at,
            url_checks.code_status,
            url_checks.created_at AS last_check, 
            url_checks.description
        FROM urls
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
    '''
    with get_db_connection() as conn:
        with conn.cursor() as curs:
            curs.execute(sql)
            urls = curs.fetchall()
            return render_template("urls.html", urls=urls)