import requests
import json, os
import urllib3
import threading
urllib3.disable_warnings()

def post(url, data,results, debug=False):
    headers = {
        "User-Agent": ""
    }
    global resp
    proxy = {
        "http": "http://127.0.0.1:8080",
        "https": "http://127.0.0.1:8080"
    }
    try:
        if debug:
            resp = requests.post(url, data, timeout=2, proxies=proxy, verify=False)
        else:
            resp = requests.post(url, data, timeout=2, verify=False)
        results += format_resp(resp)
    except:
        print("Error in requests")
        post(url, data, results)

def format_resp(resp):
    content = json.loads(resp.content)
    public_vectors_info = content["data"]
    vectors = public_vectors_info["list"]
    # count = public_vectors_info["count"]
    # current_page = public_vectors_info["current"]

    for vector in vectors:
        cid = vector['company_id']
        cname = vector['company_name']
        print("{}({})".format(cname, cid))

    return  vectors

def store2file(vectors, name):
    with open(name, "a+") as f:
        json.dump(vectors, f)


if __name__ == "__main__":
    url = "https://butian.360.cn/"
    public_vectors_path = "Reward/pub"
    vectors = []
    for i in range(173):
        body = {
            "s": 1,
            "p": i+1,
            "token": None
        }
        t = threading.Thread(target=post, args=(url+public_vectors_path, body, vectors, True))
        t.start()

    filename = "public_vectors.txt"
    if os.path.exists(filename):
        os.remove(filename)

    store2file(vectors, filename)






