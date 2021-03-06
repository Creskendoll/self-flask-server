import requests

out_file = "./temp/client.jpg"

local = "http://localhost:5000/vm/pokiki"
public = "http://www.kenansoylu.com/pokiki"
gcloud = "http://35.204.79.178:5000/pokiki"

img = "/home/ken/Pictures/a.jpg"
with open(img, 'rb') as f:
    r = requests.post(local, files={'image': f}, stream=True)
    if r.status_code == 200:
        print("Request OK")
        print("Image file path:", r.text)
        get_url = local + "?image=" + r.text # pass file location in URL args
        print("Get  URL:", get_url)
        img = requests.get(get_url)
        
        with open(out_file, 'wb') as res_file:
            res_file.write(img.content) # with GET request
            print("Saved:", out_file)
    else:
        print("Request FAIL")
        get_url = public + "?image=" + r.text # pass file location in URL args
        print("Get URL:", get_url)
        print(r.text)
