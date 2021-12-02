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
    total_pages = int(re.search('[0-9]+', wd.find_element(by="class name", value="be-pager-total").text).group())  # get the total pages
    print("total pages: {}".format(total_pages))

    _ret = []

    for page_idx in range(total_pages):
        print("page: {}".format(page_idx))
        try:
            auth_users = wd.find_elements(by="xpath", value="//li[@class='list-item clearfix']/div[@class='content']/p[@class='auth-description']/../a[@class='title']/span")
            auth_users_href = wd.find_elements(by="xpath", value="//li[@class='list-item clearfix']/div[@class='content']/p[@class='auth-description']/../a[@class='title']")
            auth_users_id = [int(re.search('[0-9]+', auth_users_href[i].get_attribute("href")).group()) for i in range(len(auth_users_href))]
            print([i.text for i in auth_users])
            wd.find_element(by="class name", value="be-pager-next").click()  # click the next page
            time.sleep(0.1)
        except Exception as e:
            print(e)
            break

    a=1

    # print(wd.find_element(by="class name", value="auth-description").text)

    # print(wd.page_source)
    soup = BeautifulSoup(wd.page_source, "html.parser")
    with open('1.html', 'w') as file_object:
        file_object.write(soup.prettify())


    return _ret


uid_source: int = 208259  # 陈睿
# uid_source: int = 546195  # 老番茄


if __name__ == "__main__":
    i = find_auth_follows(uid_source)



