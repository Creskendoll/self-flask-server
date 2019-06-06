from flask import Flask, request, abort, Response
from werkzeug.utils import secure_filename
from pathlib import Path
import json
import os
import ast
from logging import Formatter, FileHandler
import logging
from programs.Pokiki.PokikiAPI import convertFromFile, convertFromImage
from flask_cors import cross_origin
from PIL import Image
import binascii
import io

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('config')

@app.route('/pokemoned/post-image', methods=['POST'])
@cross_origin(headers=['Content-Type'])
def uploadImage():
    pokiki_program_root = Path("programs/Pokiki")
    result_images = []
    out_folder = Path("./temp/serverCache/")

    options = None
    if "options" in request.form:
        options = request.form["options"]
    else:
        options = {
            "X" : "64",
            "Y" : "64",
            "Q" : "1",
            "GetExisting" : "False",
            "SaveFile" : "True"
        }

    if type(options) is str:
        options = ast.literal_eval(options)

    for file in request.files.getlist("image"):
        file_path = os.path.join(str(out_folder.resolve()), secure_filename(file.filename))

        # print(type(file))

        # Create folder if not exists
        if not os.path.isdir(str(out_folder)):
            print("Creating folder:", str(out_folder))
            os.makedirs(str(out_folder))

        result_file = os.path.join(str(Path("./static/pokiki_images/").resolve()), secure_filename(file.filename))
        # Save file
        if options["SaveFile"] == "True":
            file.save(file_path)
            file.close()

            # if options["GetExisting"]=="True" and os.path.isfile(result_file):
            #     print("File already exists in server. Skipping program executiion.")
            # else:
            print("Starting with saving.")
            try:
                convertFromFile(file_path, options, saveTo=result_file)
            except Exception:
                return abort(500, "Subprocess failed")
            print("Result file:", result_file)
        else:
            print("Starting without saving.")
            file_bytes = file.read()
            stream = io.BytesIO(file_bytes)
            img = Image.open(stream)

            try:
                convertFromImage(img, options, saveTo=result_file)
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
    return response

@app.route('/pokemoned', methods=["GET", "POST"])
def pokikiGET():
    if request.args.get("image") is not None:
        image_path = "pokiki_images/" + request.args.get("image")
        return app.send_static_file(image_path)
    else:
        return app.send_static_file('pokemoned.html')

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
