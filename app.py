from pathlib import Path

from flask import Flask, render_template

from projects.adx_abctrainer.routes import adx_abctrainer_bp
from projects.adx_wodzefack.routes import adx_wodzefack_bp
from projects.stahh_besger import stahh_besger
from projects.stahh_besger.routes import stahh_besger_bp

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(stahh_besger_bp)
app.register_blueprint(adx_abctrainer_bp)
app.register_blueprint(adx_wodzefack_bp)

required_directories = [Path(f'{app.instance_path}')]
required_directories.extend(stahh_besger.Constants.REQUIRED_DIRS)

for dir in required_directories: # todo check permissions & properly return Errors
    if not dir.exists():
        try: # todo properly check permissions first
            Path.mkdir(dir)
        except OSError:
            pass # todo proper exception feedback

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
