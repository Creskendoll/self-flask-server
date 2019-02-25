import requests

out_file = "./temp/client.jpg"

local = "http://localhost:5000/pokiki"
public = "http://www.kenansoylu.com/pokiki"
auth = "http://www.kenansoylu.com/authCSRF"
auth = "http://localhost:5000/authCSRF"

client = requests.session()
client.get(auth)
csrf_token = client.cookies['_csrf_token']

post_data = dict(csrf_token=csrf_token, _csrf_token=csrf_token, csrfmiddlewaretoken=csrf_token, next='/')

with open('./static/images/about/02.jpg', 'rb') as f:
    r = client.post(local, files={'image': f}, stream=True, data=post_data, headers=dict(Referer=local))
    if r.status_code == 200:
        print("Request OK")
        print("Image file path:", r.text)
        get_url = local + "?image=" + r.text # pass file location in URL args
        print("Get URL:", get_url)
        img = client.get(get_url)
        
        with open(out_file, 'wb') as res_file:
            res_file.write(img.content) # with GET request
            print("Saved:", out_file)
    else:
        print("Request FAIL")
        print(r.text)
