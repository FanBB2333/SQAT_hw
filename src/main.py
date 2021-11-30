import requests
import json
import re
from bs4 import BeautifulSoup

class User:

    def __init__(self):
        self.uid: int = 0  # the number of id
        self.name: str = ""  # personal unique name
        self.intro: str = ""  # brief introduction
        self.auth_up: bool = False
        self.auth_org: bool = False


def find_auth_fans(uid: int) -> int:
    """
    :param uid: the uid of the source user
    :return: the authenticated uid list in the fans list
    """
    url = "https://space.bilibili.com/{}/fans/fans".format(uid)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    try:
        auth_id = soup.find("div", class_="zm-profile-card zm-profile-section-item zg-clear no-hovercard").find("a")["href"].split("/")[-1]
    except:
        auth_id = 0
    return auth_id

uid_source: int = 208259  # 陈睿
# uid_source: int = 546195  # 老番茄


if __name__ == "__main__":
    print("hello world".__class__)
