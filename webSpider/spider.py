#!/usr/bin/env python
# coding: utf-8

import time
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import urllib3
import requests
from urllib import response
from urllib.request import Request,urlopen
from fake_useragent import UserAgent


class spdier:
    path = 'D:\\tools\Firefox_driver\geckodriver.exe'
    # path = 'D:\\tools\Firefox_driver\geckodriver.exe'
    list_url = 'http://ceai.njnu.edu.cn/Item/list.asp?id=1652'

    # basepath = "C:\\result\\"
    basepath = "result\\"
    list_title = []
    list_link = []
    wait_time = 60

    header = {"User-Agent":UserAgent().firefox,
                  'cookie': "jS9iKARFBtYNS"
                        "=5OhtuP2LFxwHIBI2ymglfoXVJoP0IhRXHWbT8IYzxYQBPqlQw9Q6bQFGH4LBoHtRNWDcbFR1IZzlnAlWMWuoV8G; "
                        "Hm_lvt_10f0f9d6a8e84eea24952012709c66b0=1653536428,1653538138,1653656941,1653659442; "
                        "ASPSESSIONIDSQCABATS=KFJHMIPBBJFPBFGBNCOGIGPE; "
                        "jS9iKARFBtYNT=9aWEAhS5JjJabdcdbJ3tNT9EFTQpZ2HOAUvzrJU83dEn1DjKGBmaG_YfsklpHNQ2eVu6FFKJcqYKi5rkUKxzVM9ZU5wjhL17Q2thC.WBIhL3mm6zKHbsMOM9pQQ80JGjj0WmwVxIDU51yIxY97CcbjWB_AmxO0OShW4iLNpDJMhdzbi28QMEkZ7tCVQ1py9WunjKkkVTy2gBVH0AYE5dEmc7Fgz_TdWvj6Tfp1yqGTdhuMI8SZBy5agX8rn2MO3LCfJYbOsAfDKECxiSsEpi6NeNrjXTp31EGxCooCm.JTvVqK7zObm9pzc0YShcJvRMVKQwmviu1GS.WqYzXs3zyE8Ktxk1jc8BinynDlfqx9l"}
    firefox_option = Options()
    firefox_option.add_argument('--headless')
    firefox_option.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')

    firefox_option.set_capability("unhandledPromptBehavior", "accept")
    desired_capabilities = DesiredCapabilities.FIREFOX
    desired_capabilities["pageLoadStrategy"] = "none"
    firefox_profile = webdriver.FirefoxProfile()
    # 禁用图片
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('browser.migration.version', 9001)
    # 禁用css
    firefox_profile.set_preference('permissions.default.stylesheet', 2)
    # 禁用flash
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    # 禁用js
    firefox_profile.set_preference('javascript.enabled', 'false')

    driver = webdriver.Firefox(options=firefox_option,desired_capabilities=desired_capabilities,firefox_profile=firefox_profile)
    # driver.set_script_timeout(1)
    # driver.set_page_load_timeout(1)
    wait=WebDriverWait(driver, wait_time, poll_frequency=0.5, ignored_exceptions=None)



    def get_title(self, start,page_nums):
        print('开始获取文档')
        file_title_list = open(spdier.basepath + "title_list.txt", "w")
        file_link_list = open(spdier.basepath + "link_list.txt", "w")
        new_nums = 0
        for i in range(start, page_nums):
            spdier.driver.get(spdier.list_url + '&page=%d'%i)
            time.sleep(0.4)
            a_s = spdier.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.content-list > ul > li > span > a')))
            for a in a_s:
                new_nums=new_nums+1
                spdier.list_title.append(a.text)
                spdier.list_link.append(a.get_attribute('href'))
        for title in spdier.list_title:
            file_title_list.write(title)
            file_title_list.write('\n')
        for link in spdier.list_link:
            file_link_list.write(link)
            file_link_list.write('\n')
        file_link_list.close()
        file_title_list.close()
        print('共解析通知%d页，共%d条'%(page_nums,new_nums))

    def get_link_from_file(self):
        for line in open(spdier.basepath + "link_list.txt",'r'):
            if line!='\n':
                spdier.list_link.append(line)
        print("地址解析完毕")
        

    def get_all_news(self,start,end):
        for i in range(start,end):
            link = spdier.list_link[i]
            # resp = requests.request(url=link,method='get',headers=spdier.header)
            # print(resp.status_code)
            # rep = urllib.request.urlopen(link,headers=spdier.header)
            # if(rep.)
            # print(myURL1.getcode())  # 200
            #
            # try:
            #     myURL2 = urllib.request.urlopen("https://www.runoob.com/no.html")
            # except urllib.error.HTTPError as e:
            #     if e.code == 404:
            #         print(404)  # 404
            try:
                spdier.driver.get(link)
                # time.sleep(0.5)
            except:
                print("访问超时 %s" %link)
                i=i+1
                link = spdier.list_link[i]
            try:
                ps = spdier.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,'#MyContent > p')))
            except StaleElementReferenceException as SE:
                print(SE)
                ps = spdier.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#MyContent > p')))

            # 写入内容
            with open(spdier.basepath +'row_news\\'+  '%d.txt' % i, "w",encoding='utf-8') as content_file:
                for p in ps:
                    content_file.write(p.text)
            content_file.close()
            print('第%d条新闻 %s 读取完毕' % (i,link))


        print("爬取完毕，共爬取文档%d条"%i)
        spdier.driver.close()

