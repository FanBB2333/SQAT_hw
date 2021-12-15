from typing import List

import requests
import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import sys

from selenium.webdriver.chrome.options import Options
_options = Options()
_options.add_argument('--headless')


def find_auth_follows(uid: int) -> List[int]:
    """
    find the authenticated users among the user's follows
    :param uid: the uid of the source user
    :return: the authenticated uid list in the follow list
    """
    url = "https://space.bilibili.com/{}/fans/follow".format(uid)
    wd = webdriver.Chrome(options=_options)
    # wd = webdriver.Chrome()

    wd.get(url)
    time.sleep(2)
    try:
        total_pages = int(re.search('[0-9]+', wd.find_element(by="class name", value="be-pager-total").text).group())  # get the total pages
    except Exception as e:
        print("由于该用户隐私设置，关注列表不可见")
        # print(e)
        return []

    print("total pages: {}".format(total_pages))

    _ret = []

    for page_idx in range(min(total_pages, 5)):
        print("page: {}".format(page_idx+1))
        try:
            auth_users = wd.find_elements(by="xpath", value="//li[@class='list-item clearfix']/div[@class='content']/p[@class='auth-description']/../a[@class='title']/span")
            auth_users_href = wd.find_elements(by="xpath", value="//li[@class='list-item clearfix']/div[@class='content']/p[@class='auth-description']/../a[@class='title']")
            auth_users_id = [int(re.search('[0-9]+', auth_users_href[i].get_attribute("href")).group()) for i in range(len(auth_users_href))]
            _ret.extend([i for i in auth_users_id])
            print([i.text for i in auth_users])
            # the last page does not need to go to next one
            if page_idx != total_pages-1:
                wd.find_element(by="class name", value="be-pager-next").click()  # click the next page
            time.sleep(0.3)
        except Exception as e:
            print("error in uid: {} and page: {}".format(uid, page_idx))
            print(e)
            # break

    # soup = BeautifulSoup(wd.page_source, "html.parser")
    # with open('1.html', 'w') as file_object:
    #     file_object.write(soup.prettify())
    print("Found {} auth users from {}".format(len(_ret), uid))


    return _ret


# uid_source: int = 208259  # 陈睿
# uid_source: int = 546195  # 老番茄
uid_source: int = 946974  # 影视飓风
# uid_source: int = 12590  # epcdiy

# uid_source = 6330633


class User:

    def __init__(self, uid: int):
        self.uid: int = uid  # the number of id
        self.name: str = ""  # personal unique name
        self.intro: str = ""  # brief introduction
        self.follows: str = 0  # the number of follows
        self.fans: str = 0  # the number of fans
        self.contributions: str = 0  # the number of contributions
        self.top_playlist: List[str] = []  # the list of play list
        self.auth_up: bool = False
        self.auth_org: bool = False
        self.auth_follows: List[int] = find_auth_follows(uid)  # the list of authenticated users among the user's follows
        # TODO: complete the other attributes
        url_main = "https://space.bilibili.com/{}".format(uid)
        # wd = webdriver.Chrome(options=_options)
        wd = webdriver.Chrome()

        wd.get(url_main)
        time.sleep(1)
        self.name = wd.find_element(by="xpath", value="/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[1]/span[1]").text
        self.intro = wd.find_element(by="xpath", value="/html/body/div[2]/div[1]/div[1]/div[2]/div[2]/div/div[2]/div[2]/h4").text
        self.follows = wd.find_element(by="xpath", value="/html/body/div[2]/div[2]/div/div[1]/div[3]/a[1]/p[2]").text
        self.fans = wd.find_element(by="xpath", value="/html/body/div[2]/div[2]/div/div[1]/div[3]/a[2]/p[2]").text

        url_contributions = "https://space.bilibili.com/{}/video".format(uid)
        wd.get(url_contributions)
        time.sleep(1)
        self.contributions = wd.find_element(by="xpath", value="/html/body/div[2]/div[2]/div/div[1]/div[1]/a[3]/span[3]").text
        for idx in range(1, 6):
            video_xpath = "/html/body/div[2]/div[4]/div/div/div[2]/div[4]/div/div/ul[2]/li[{}]/a[2]".format(idx)
            self.top_playlist.append(wd.find_element(by="xpath", value=video_xpath).text)

        soup = BeautifulSoup(wd.page_source, "html.parser")
        with open('1.html', 'w') as file_object:
            file_object.write(soup.prettify())


    def __eq__(self, other):
        return self.uid == other.uid

if __name__ == "__main__":

    a = User(uid_source)
    sys.exit(0)

    # find_auth_follows(uid_source)
    all_users: List[User] = []
    added_users = {}
    all_users.append(User(uid_source))
    added_users[uid_source] = True

    iteration = 5
    for i in range(iteration):
        print("iteration: {}. There are {} users in total.".format(i, len(all_users)))
        to_be_extend = []
        # collect the authed users to be extended
        for u in all_users:
            to_be_extend.extend(u.auth_follows)
        print("to be extended: {}".format(to_be_extend))
        for uid in to_be_extend:
            if uid not in added_users:
                all_users.append(User(uid))
                added_users[uid] = True

    print("At last there are {} users in total.".format(len(all_users)))





