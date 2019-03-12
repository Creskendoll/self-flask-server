#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, send_file, abort, Blueprint
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import subprocess

from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFProtect
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# csrf = CSRFProtect(app)
# api_blueprint = Blueprint('api', __name__)
# csrf.exempt(api_blueprint)
# app.register_blueprint(api_blueprint)
# api = restful.Api(app, decorators=[csrf_protect.exempt])
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return app.send_static_file("index.html")

@app.route('/pokiki', methods=['POST'])
def pokiki():
    pokiki_program_root = Path("programs/Pokiki")
    print("Pokiki root:", pokiki_program_root.resolve())

    f = None
    if "image" in request.files:
        f = request.files['image']
    else:
        return "No image provided"

    if f is not None:
        out_folder = Path("./temp/serverCache/")
        print("received IMG:", f.filename)
        file_path = os.path.join(str(out_folder.resolve()), secure_filename(f.filename))

        f.save(file_path)
        print("Saved to:", file_path)

        pokiki_program = pokiki_program_root / "Program.py"

        result_file = os.path.join(str(Path("./static/programFiles/").resolve()), secure_filename(f.filename))

        print("Result file:", result_file)
        if not os.path.isfile(result_file):
            subprocess.run(["python", str(pokiki_program.resolve()), "-i", file_path, "-o", result_file])
        else:
            print("File already exists in server. Skipping program executiion.")
        
        if os.path.isfile(result_file):
            img_path = "programFiles/" + secure_filename(f.filename)
            return str(img_path)
        else:
            return abort(500)
    else:
        return "can't process image"

# Error handlers.
@app.route('/pokiki', methods=["GET"])
def pokikiGET():
    if request.args.get("image") is not None:
        return app.send_static_file(request.args.get("image"))
    else:
        return app.send_static_file('pokiki.html')

@app.errorhandler(404)
def not_found_error(error):
    return app.send_static_file("404.html"), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)