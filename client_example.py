import requests

out_file = "./temp/client.jpg"

local = "http://localhost:5000/pokiki"
public = "http://www.kenansoylu.com/pokiki"
gcloud = "https://titanium-acumen-232511.appspot.com/pokiki"
gcloud = "http://35.198.148.117:5000/pokiki"

img = "D:\Code\BAU\IMG\pokiki\in\sevval.jpg"
# './static/images/about/02.jpg'
with open(img, 'rb') as f:
    r = requests.post(gcloud, files={'image': f}, stream=True)
    if r.status_code == 200:
        print("Request OK")
        print("Image file path:", r.text)
        get_url = gcloud + "?image=" + r.text # pass file location in URL args
        print("Get URL:", get_url)
        img = requests.get(get_url)
        
        with open(out_file, 'wb') as res_file:
            res_file.write(img.content) # with GET request
            print("Saved:", out_file)
    else:
        print("Request FAIL")
        get_url = public + "?image=" + r.text # pass file location in URL args
        print("Get URL:", get_url)
        print(r.text)
