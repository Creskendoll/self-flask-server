import requests

# server IP
server_url = "http://35.198.148.117:5000/pokiki"
# If it doesn't work try this
# server_url = "http://www.kenansoylu.com/pokiki"

input_img_path = "<YOUR PATH IMAGE HERE>"
output_img_save_path "<YOUR SAVE PATH HERE>"

with open(input_img_path, 'rb') as f:
    # POST request
    r = requests.post(server_url, files={'image': f}, stream=True)
    if r.status_code == 200:
        print("Request OK")
        print("Image file path:", r.text)
        get_url = server_url + "?image=" + r.text 
        print("Get URL:", get_url)
        # Result image
        img = requests.get(get_url)
        # Save as file
        with open(output_img_save_path, 'wb') as res_file:
            res_file.write(img.content) # with GET request
            print("Saved to:", output_img_save_path)
    else:
        # Request failed
        print("Request FAIL")
        get_url = public + "?image=" + r.text 
        print("Get URL:", get_url)
        print(r.text)
