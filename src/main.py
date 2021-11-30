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
        self.follows: int = 0  # the number of follows
        self.fans: int = 0  # the number of fans
        self.auth_up: bool = False
        self.auth_org: bool = False


def find_auth_follows(uid: int) -> List[int]:
    """
    find the authenticated users among the user's follows
    :param uid: the uid of the source user
    :return: the authenticated uid list in the follow list
    """
    url = "https://space.bilibili.com/{}/fans/follow".format(uid)
    wd = webdriver.Chrome(options=_options)

    wd.get(url)
    # wd.find_element(by="class name", value="be-pager-total")
    print(wd.find_element(by="class name", value="be-pager-total").text)
    print(wd.find_element(by="class name", value="auth-description").text)

    wd.find_element(by="class name", value="be-pager-next").click()
    # print(wd.page_source)
    soup = BeautifulSoup(wd.page_source, "html.parser")
    with open('1.html', 'w') as file_object:
        file_object.write(soup.prettify())
    print(soup.prettify())

    _ret = []

    return _ret


uid_source: int = 208259  # 陈睿
# uid_source: int = 546195  # 老番茄


if __name__ == "__main__":
    i = find_auth_follows(uid_source)



