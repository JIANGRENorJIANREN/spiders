from selenium import webdriver
import time

def weibo_qq_login():
    driver = webdriver.Firefox()
    driver.get('https://weibo.com/')
    time.sleep(4)

    driver.find_element_by_css_selector('div.info_list.other_login.clearfix div.other_login_list.W_fl a.cp_logo.icon_qq').click()
    time.sleep(2)

    driver.switch_to_window(driver.window_handles[1])
    time.sleep(1)

    driver.get(driver.current_url)

    driver.switch_to_frame('ptlogin_iframe')

    driver.find_element_by_css_selector('div#bottom_qlogin.bottom.hide a#switcher_plogin.link').click()
    time.sleep(1)

    driver.find_element_by_css_selector('div#uinArea.uinArea div.inputOuter input#u.inputstyle').send_keys('765155479@qq.com')

    driver.find_element_by_css_selector('div.inputOuter input#p.inputstyle.password').send_keys('888841520')

    driver.find_element_by_css_selector('input#login_button.btn').click()

if __name__ == '__main__':
    weibo_qq_login()