from typing import List

import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time


from selenium.webdriver.chrome.options import Options
_options = Options()
_options.add_argument('--headless')


class User:

    def __init__(self):
        self.uid: int = 0  # the number of id
        self.name: str = ""  # personal unique name
        self.intro: str = ""  # brief introduction
        self.auth_up: bool = False
        self.auth_org: bool = False


def find_auth_fans(uid: int) -> List[int]:
    """
    :param uid: the uid of the source user
    :return: the authenticated uid list in the fans list
    """
    url = "https://space.bilibili.com/{}/fans/fans".format(uid)
    wd = webdriver.Chrome(options=_options)

    wd.get(url)
    # print(wd.page_source)
    soup = BeautifulSoup(wd.page_source, "html.parser")
    print(soup.prettify())

    _ret = []

    return _ret


uid_source: int = 208259  # 陈睿
# uid_source: int = 546195  # 老番茄


if __name__ == "__main__":
    i = find_auth_fans(uid_source)



