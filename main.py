#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request, send_file, abort, Response
import logging
from logging import Formatter, FileHandler
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import subprocess
import io
import requests
import ast
from flask_cors import CORS, cross_origin
import json

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

@app.route("/cloud-applications")
def hw():
    return app.send_static_file("cloudApp.html")

@app.route('/')
def home():
    return app.send_static_file("index.html")

@cross_origin(headers=['Content-Type'])
@app.route('/vm/<path:path>', methods=['POST', 'GET'])
def _proxy(path):
    vm_URL = "http://35.204.79.178:5000"
    # vm_URL = "http://localhost:5000"

    # print("PATH URL:", path)
    # print("HOST URL:", request.host_url)
    # print("Request URL:", request.url)
    redirect_url = request.url.replace(request.host_url+"vm", vm_URL)    
    # print("Redirect URL:", redirect_url)

    resp = requests.request(
        method=request.method,
        url=redirect_url,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response

@app.route('/pokemoned', methods=['GET'])
def pokemoned():
    return app.send_static_file("pokemoned.html")

@app.route('/pokemoned/post-image', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def uploadImage():
    pokiki_program_root = Path("programs/Pokiki")
    result_images = []
    out_folder = Path("./temp/serverCache/")
    for file in request.files.getlist("image"):
        # Save file
        file_path = os.path.join(str(out_folder.resolve()), secure_filename(file.filename))
        if not os.path.isdir(out_folder):
            print("Creating folder:", out_folder)
            os.makedirs(out_folder)
        file.save(file_path)
        file.close()

        options = None
        if "options" in request.form:
            options = request.form["options"]
        else:
            options = {
                "X" : "64",
                "Y" : "64",
                "Q" : "1",
                "GetExisting" : "False"
            }

        if type(options) is str:
            options = ast.literal_eval(options)

        pokiki_program = pokiki_program_root / "Program.py"

        result_file = os.path.join(str(Path("./static/pokiki_images/").resolve()), secure_filename(file.filename))

        # if options["GetExisting"]=="True" and os.path.isfile(result_file):
        #     print("File already exists in server. Skipping program executiion.")
        # else:
        print("Starting program.")
        try:
            subprocess.run(["python3", str(pokiki_program.resolve()), "-i", file_path, "-o", result_file, 
                            "-x", options["X"], "-y", options["Y"], "-q", options["Q"]])
        except Exception:
            return abort(500, "Subprocess failed")
        print("Result file:", result_file)

        if os.path.isfile(result_file):
            result_images.append(secure_filename(file.filename))
        else:
            return abort(500, "File couldn't be found")

    res = {
        "images" : result_images
    }
    response = app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    # return app.send_static_file("pokiki_images/" + secure_filename(files[0].filename))
    return response

@app.route('/pokiki', methods=['POST'])
def pokiki():
    pokiki_program_root = Path("programs/Pokiki")
    #print("Pokiki root:", pokiki_program_root.resolve())
    
    f = None
    if "image" in request.files:
        f = request.files['image']
    else:
        return abort(400, "No image provided")
        
    options = None
    if "options" in request.form:
        options = request.form["options"]
    else:
        options = {
            "X" : "150",
            "Y" : "100",
            "Q" : "4",
            "GetExisting" : "False"
        }

    if type(options) is str:
        options = ast.literal_eval(options)

    if f is not None:
        out_folder = Path("./temp/serverCache/")
        print("received IMG:", f.filename)
        if not os.path.isdir(out_folder):
            print("Creating folder:", out_folder)
            os.makedirs(out_folder)
        file_path = os.path.join(str(out_folder.resolve()), secure_filename(f.filename))

        # Save file 
        in_memory_file = io.BytesIO(f.read())
        with open(file_path,'wb') as out: ## Open temporary file as bytes
            out.write(in_memory_file.read())                ## Read bytes into file
        print("Saved to:", file_path)

        pokiki_program = pokiki_program_root / "Program.py"

        result_file = os.path.join(str(Path("./static/pokiki_images/").resolve()), secure_filename(f.filename))

        if options["GetExisting"]=="True" and os.path.isfile(result_file):
            print("File already exists in server. Skipping program executiion.")
        else:
            print("Starting program.")
            try:
                subprocess.run(["python3", str(pokiki_program.resolve()), "-i", file_path, "-o", result_file, 
                                "-x", options["X"], "-y", options["Y"], "-q", options["Q"]])
            except Exception:
                return abort(500, "Subprocess failed")
            print("Result file:", result_file)
        
        if os.path.isfile(result_file):
            img_path = secure_filename(f.filename)
            return str(img_path)
        else:
            return abort(500, "File couldn't be found")
    else:
        return abort(500, "Error getting file")

# Error handlers.
@app.route('/pokiki', methods=["GET"])
def pokikiGET():
    if request.args.get("image") is not None:
        image_path = "pokiki_images/" + request.args.get("image")
        return app.send_static_file(image_path)
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)