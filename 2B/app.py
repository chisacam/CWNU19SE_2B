from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/weather')
def weather_page():
    return render_template("/weather.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
