import requests
import shutil

out_file = "./temp/client.jpg"

with open('./static/images/logo/favicon.png', 'rb') as f:
    r = requests.post('http://self-flask-server-eu.herokuapp.com/pokiki', files={'image': f}, stream=True)
    if r.status_code == 200:
        print("Request OK")
        with open(out_file, 'wb') as res_file:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, res_file)
            print("Saved:", out_file)
    else:
        print(r.text)