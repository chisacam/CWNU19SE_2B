from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def main_page():
    return render_template("index.html")


@app.route('/weather')
def weather_page():
    return render_template("weather.html")


@app.route('/searchRecent')
def recent_search():
    return render_template("search_recent.html")


@app.route('/searchBookmark')
def recent_bookmark():
    return render_template("search_bookmark.html")


@app.route('/searchText')
def search_text():
    return render_template("search_text.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0')
