import selenium
from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class spdier:
    path = 'D:\\tools\Firefox_driver\geckodriver.exe'
    # path = 'D:\\tools\Firefox_driver\chromedriver.exe'
    list_url = 'http://ceai.njnu.edu.cn/Item/list.asp?id=1652'
    list_xpath = '/html/body/div[2]/div/div/div[2]/div[2]/div/ul'
    content_xpath = '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div[2]/div/p[2]/span'
    basepath = "D:\文件\大三下\数据挖掘\webSpider\\result\\"
    list_title = []
    list_link = []
    wait_time = 600

    firefox_option = Options()
    firefox_option.add_argument('--headless')
    firefox_option.add_argument('user-agent="Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"')

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

    driver = webdriver.Firefox(service=Service(executable_path=path),options=firefox_option,desired_capabilities=desired_capabilities,firefox_profile=firefox_profile)
    wait=WebDriverWait(driver, wait_time, poll_frequency=0.5, ignored_exceptions=None)

    def get_title(self, start,page_nums):
        print('开始获取文档')
        file_title_list = open(spdier.basepath + "title_list.txt", "w")
        file_link_list = open(spdier.basepath + "link_list.txt", "w")
        # .content - list > ul: nth - child(2) > li:nth - child(1) > span: nth - child(1) > a:nth - child(1)
        # .content - list > ul: nth - child(2) > li:nth - child(2) > span: nth - child(1) > a:nth - child(1)
        new_nums = 0
        for i in range(start, page_nums):
            # spdier.driver.implicitly_wait(600)
            spdier.driver.get(spdier.list_url + '&page=%d' % i)
            # title_lis = spdier.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '.content-list > ul:nth-child(2)>li')))
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
            print('第%d页 网页地址解析完毕' % i)
        file_link_list.close()
        file_title_list.close()
        print('共解析通知%d页，共%d条'%(page_nums,new_nums))

    def get_link_from_file(self):
        for line in open(spdier.basepath + "link_list.txt",'r'):
            if line!='\n':
                spdier.list_link.append(line)
        print("地址解析完毕")

    def get_all_news(self,start,end):
        # spdier.driver.implicitly_wait(600)

        for i in range(start,end):
            link = spdier.list_link[i]
            spdier.driver.get(link)
            try:
                ps = spdier.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR,'#MyContent > p')))
            except StaleElementReferenceException as SE:
                ps = spdier.wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, '#MyContent > p')))
            with open(spdier.basepath + 'news\\' + '%d.txt' % i, "w",encoding='utf-8') as content_file:
                for p in ps:
                    content_file.write(p.text)
            content_file.close()
            print('第%d条新闻 %s 读取完毕' % (i,link))
        print("爬取完毕，共爬取文档%d条"%i)