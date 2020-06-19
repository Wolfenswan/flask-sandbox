from flask import Flask, render_template

from config import Config
from projects.adx_abctrainer.routes import adx_abctrainer
from projects.higo_starbesger.routes import higo_starbgesger

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(higo_starbgesger)
app.register_blueprint(adx_abctrainer)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()