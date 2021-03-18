from flask import Flask, url_for, render_template
import os


app = Flask(__name__)

@app.route('/')
def index():
    script = url_for('static', filename='main.js')
    stylesheet = url_for('static', filename='stylesheet.css')
    return render_template('index.html', script=script, stylesheet=stylesheet)


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG_MODE", True), host='0.0.0.0')