#!/usr/bin/env python
# coding: utf-8

import time
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException, TimeoutException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class spdier:
    path = 'D:\\tools\Firefox_driver\geckodriver.exe'
    list_url = 'http://ceai.njnu.edu.cn/Item/list.asp?id=1652'
    basepath = "result\\"
    list_title = []
    list_link = []
    wait_time = 60
    fail_nums = 0


    def __init__(self):
        firefox_option = Options()
        firefox_option.add_argument('--headless')
        firefox_option.add_argument(
            'user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')
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
        self.driver = webdriver.Firefox(options=firefox_option, desired_capabilities=desired_capabilities,
                                   firefox_profile=firefox_profile)
        self.wait = WebDriverWait(self.driver, self.wait_time, poll_frequency=0.5, ignored_exceptions=None)



    def get_title(self, start,page_nums):
        print('开始获取文档标题与链接......')
        file_title_list = open(self.basepath + "title_list.txt", "w")
        file_link_list = open(self.basepath + "link_list.txt", "w")
        new_nums = 0
        for i in range(start, page_nums):
            self.driver.get(self.list_url + '&page=%d'%i)
            time.sleep(0.4)
            a_s = self.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.content-list > ul > li > span > a')))
            for a in a_s:
                new_nums=new_nums+1
                self.list_title.append(a.text)
                self.list_link.append(a.get_attribute('href'))
        for title in spdier.list_title:
            file_title_list.write(title)
            file_title_list.write('\n')
        for link in self.list_link:
            file_link_list.write(link)
            file_link_list.write('\n')
        file_link_list.close()
        file_title_list.close()
        print('共解析通知%d页，共%d条'%(page_nums,new_nums))

    def get_link_from_file(self):
        for line in open(spdier.basepath + "link_list.txt",'r'):
            if line!='\n':
                self.list_link.append(line)
        print("地址解析完毕")
        

    def get_all_news(self,start,end):
        for i in range(start,end):
            try:
                link = spdier.list_link[i]
                flag = True
                while flag:
                    try:
                        self.driver.get(link)
                        time.sleep(0.4)
                        flag = False
                    except:
                        print("访问超时 %s" %link)
                        i=i+1
                        link = self.list_link[i]
                try:
                    ps = self.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,'#MyContent > p')))
                    with open(self.basepath + 'row_news\\' + '%d.txt' % i, "w", encoding='utf-8') as content_file:
                        for p in ps:
                            content_file.write(p.text)
                    content_file.close()
                    print('第%d条新闻 %s 读取完毕' % (i, link))
                except StaleElementReferenceException as SE:
                    print(SE)
                    ps = self.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#MyContent > p')))
                except TimeoutException as TE:
                    self.fail_nums = self.fail_nums+1
                    print('读取失败404: %s'%link)
            except IndexError:
                print("爬取完毕，共爬取文档%d条,爬取失败%d条"%(i,self.fail_nums))
                break
        self.driver.close()

