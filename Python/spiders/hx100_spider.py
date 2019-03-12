# coding:utf-8
"""
Spider the hx100.com just for os video
"""
import re
import os
import pickle
from bs4 import BeautifulSoup
from requests import Session


script_path = os.path.dirname(os.path.realpath(__file__))
resource_dir = "resources"
host = "hxx100.com"
schema = "http://"
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

headers = {
    "user-agent": """Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36""",
}

start_url = 'http://hxx100.com/player.php?player=pptplayer&mov_id=4318&look_id=1'
login_url = "http://hxx100.com/user.php?act=signin"
loginout_url = "http://hxx100.com/user.php?act=logout"

user_info = {
    'username': 'xxx',
    'password': 'xxxx'
}

resource_files = "/tmp/locaions.res"

def capture_url(re_target, to_string):
    matches = re_target.search(to_string)
    if matches:
        link = matches.groups()[0]
    else:
        link = None
    return link

def check_url(link):
    if link.startswith(schema):
        return True
    else:
        return False

if __name__ == "__main__":

    s = Session()
    resp = s.post(login_url,data=user_info, proxies=proxies)
    resp_set_cookie = resp.headers["set-Cookie"]

    if "sessionhash" in resp_set_cookie:
        print("Login successfully! ")

    resp = s.get(start_url, proxies=proxies)
    resources = list()

    soup = BeautifulSoup(resp.text, "html.parser")
    a_tags = soup.select("ul.player li a")

    for a_tag in a_tags:
        resource = dict()
        link = schema + host + "/" + a_tag['href']

        name = a_tag.contents[0].replace(" ", "_")
        resource["name"] = name
        resource["link"] = link
        resources.append(resource)

    if not os.path.exists(resource_files):
        for resource in resources:
            resp = s.get(resource["link"], proxies=proxies)

            iframe_re = re.compile(r'<iframe.*src="([^"]*)"')
            link = capture_url(iframe_re, resp.text)
            if  not check_url(link):
                link = schema + host + link

            resp = s.get(link, proxies=proxies)

            video_re = re.compile('<video.*src="([^"]*)"')
            link = capture_url(video_re, resp.text)

            resp = s.get(link, allow_redirects=False, proxies=proxies)
            location = resp.headers["Location"]

            resource["location"] = location

        with open(resource_files, "wb") as f:
            pickle.dump(resources, f)
    else:
        with open(resource_files, 'rb') as f:
            resources = pickle.load(f)

    real_path = script_path + os.path.sep + resource_dir
    if os.path.exists(real_path):
        pass
    else:
        os.mkdir(resource_dir, mode=0o755)

    for index, resource in enumerate(resources):
        index = str(index)
        if len(index) < 2:
            index = "0" + index
        name = real_path + os.path.sep + index + resource['name'] + ".mp4"

        if os.path.exists(name):
            print("文件已下载")
        else:
            resp = s.get(resource["location"], proxies=proxies)
            with open(name, 'wb') as f:
                f.write(resp.content)
