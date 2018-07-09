# -*- coding:utf-8 -*-

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time


def login():
    seed_url = 'https://www.taobao.com'
    driver = webdriver.Firefox()
    driver.get(seed_url)
    # 跳转到登录页面
    driver.find_element_by_css_selector('div.site-nav-sign a.h').click()
    time.sleep(1)
    # 切换为'密码登录'
    driver.find_element_by_css_selector('div#J_QRCodeLogin.qrcode-login div.login-links a.forget-pwd.J_Quick2Static').click()
    # input username
    driver.find_element_by_css_selector('input#TPL_username_1').clear()
    driver.find_element_by_css_selector('input#TPL_username_1').send_keys('进入无愁')
    time.sleep(5)
    # input password
    driver.find_element_by_css_selector('input#TPL_password_1').clear()
    driver.find_element_by_css_selector('input#TPL_password_1').send_keys('wo198612')
    time.sleep(3)

    # 点击登录按钮
    driver.find_element_by_css_selector('button#J_SubmitStatic.J_Submit').click()


    driver.find_element_by_css_selector('input#TPL_password_1').clear()
    driver.find_element_by_css_selector('input#TPL_password_1').send_keys('wo198612')

    while True:
        button = driver.find_element_by_id('nc_1_n1z')  # 找到“蓝色滑块”
        time.sleep(1)
        action = ActionChains(driver)  # 实例化一个action对象
        action.click_and_hold(button).perform()  # perform()用来执行ActionChains中存储的行为
        time.sleep(1)
        action.reset_actions()
        action.move_by_offset(258, 0).perform()  # 移动滑块
        time.sleep(5)

        try:
            result_fail = driver.find_element_by_css_selector('div#nocaptcha.nc-container.tb-login div.errloading span.nc-lang-cnt a')
            result_fail.click()
        except NoSuchElementException:
            pass

        try:
            result_success = driver.find_element_by_css_selector('div#nc_1__scale_text.scale_text.nc-align-center.scale_text2 span.nc-lang-cnt b')
            break
        except NoSuchElementException:
            pass


    time.sleep(1)  #等待停顿时间

    driver.find_element_by_css_selector('button#J_SubmitStatic.J_Submit').click()

    print(driver.page_source)

if __name__ == '__main__':
    login()