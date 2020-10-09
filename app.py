from flask import Flask, render_template

from config import Config
from projects.adx_abctrainer.routes import adx_abctrainer
from projects.stahh_besger.routes import stahh_besger

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(stahh_besger)
app.register_blueprint(adx_abctrainer)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
