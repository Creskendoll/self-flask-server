import requests
import shutil

out_file = "./temp/client.jpg"

local = "http://localhost:5000/pokiki"
public = "http://www.kenansoylu.com/pokiki"

with open('./static/images/about/02.jpg', 'rb') as f:
    r = requests.post(local, files={'image': f}, stream=True)
    if r.status_code == 200:
        print("Request OK")
        print("Image file path:", r.text)
        get_url = local + "?image=" + r.text # pass file location in URL args
        print("Get URL:", get_url)
        img = requests.get(get_url)
        
        with open(out_file, 'wb') as res_file:
            # r.raw.decode_content = True
            # shutil.copyfileobj(r.raw, res_file)
            # img.content.decode_content = True
            res_file.write(img.content) # with GET request
            # shutil.copyfileobj(img.content, res_file)
            print("Saved:", out_file)
    else:
        print("Request FAIL")
        print(r.text)
