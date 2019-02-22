import requests
import shutil

out_file = "./temp/client_out.jpg"

with open('./static/images/about/02.jpg', 'rb') as f:
    r = requests.post('http://192.168.0.56:5000/pokiki', files={'image': f}, stream=True)
    if r.status_code == 200:
        with open(out_file, 'wb') as res_file:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, res_file)