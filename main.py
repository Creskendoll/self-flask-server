#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, request, Response
import logging
from logging import Formatter, FileHandler
import os
import requests
from flask_cors import cross_origin

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('config')

VM_URL = "http://35.204.158.54:5001"
# VM_URL = "http://localhost:5001"

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

def proxy(redirect_url):

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

@cross_origin(headers=['Content-Type'])
@app.route('/vm/<path:path>', methods=['POST', 'GET'])
def vm(path):

    redirect_url = request.url.replace(request.host_url+"vm", VM_URL)

    return proxy(redirect_url)

@app.route('/pokemoned', methods=["GET"])
@cross_origin(headers=['Content-Type'])
def pokikiGET():
    if request.args.get("image") is not None:

        redirect_url = VM_URL + "/pokemoned?image=" + request.args.get("image")

        return proxy(redirect_url)
    else:
        return app.send_static_file('pokemoned.html')
        
@app.route('/pokemoned/post-image', methods=["POST"])
@cross_origin(headers=['Content-Type'])
def postImg():
    redirect_url = VM_URL + "/pokemoned/post-image"
    return proxy(redirect_url)
        
# Error handlers.
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
    