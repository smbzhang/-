#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    else:
        pass


class AttackOnTitanSpider:

    def __init__(self, series):
        self.base_url = "https://manhua.fzdm.com/39/{}/index_{}.html"
        self.base_url_96 = "https://manhua.fzdm.com/39/0{}/index_{}.html"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }
        self.pages_number = 0
        self.series = series
        self.save_path = "./" + str(self.series)
        mkdir(self.save_path)

        # 初始化 seleniums 组件  下面三行可以使得浏览器不弹出自动化测试的拦截窗口
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')  # 关闭自动化程序运行的提示
        # option.add_argument('--headless')      #隐藏浏览器窗口
        self.driver = webdriver.Chrome(options=option)
        pass

    def get_pages_number(self):
        for pn in range(1, 100):
            if self.series == 96:
                url = self.base_url_96.format(self.series, pn)
            else:
                url = self.base_url.format(self.series, pn)
            response = requests.get(
                url=url,
                headers=self.headers
            )
            status_code = response.status_code
            if status_code != 200:
                self.pages_number = pn - 1
                break
        pass
    
    def get_url_list(self):
        self.get_pages_number()
        print(self.pages_number)
        url_list = []
        for pn in range(1, self.pages_number+1, 1):
            if self.series == 96:
                url = self.base_url_96.format(self.series, pn)
            else:
                url = self.base_url.format(self.series, pn)
            url_list.append(url)
        self.pages_number = 0
        return url_list

    def get_content(self, url):
        response = requests.get(
            url=url,
            headers=self.headers
        )
        return response.content.decode("utf-8")

    def get_images_by_selenium(self, url, index):
        self.driver.get(url)
        try:
            img_path = self.driver.find_element_by_xpath(".//img[@id='mhpic']")
            img_url = img_path.get_attribute('src')
            img_content = requests.get(img_url, self.headers).content
            img_name = self.save_path + '/' + str(index) + '.jpg'
            with open(img_name, 'wb') as file:
                file.write(img_content)
                file.flush()
            file.close()
            # time.sleep(1)
            pass
        except NoSuchElementException:
            pass

    def get_images(self, content, index):
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find_all('img')
        return items
        pass

    def run(self):
        # 1. 获取 url 列表
        url_list = self.get_url_list()
        for url in url_list:
            # 2. 发送请求获取响应
            # content = self.get_content(url)
            # 3. 从响应中提取数据
            self.get_images_by_selenium(url, url_list.index(url) + 1)
            # # 4. 保存数据
            # self.save_items(items)
        pass


if __name__ == '__main__':
    # for series in range(91, 107):
    #     spider = AttackOnTitanSpider(series)
    #     spider.run()
    spider = AttackOnTitanSpider(96)
    spider.run()
