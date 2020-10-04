from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from urllib.parse import quote
import time
import warnings
warnings.filterwarnings('ignore')


def login(driver, userName, password):
    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'
    driver.get(f'https://portal.pku.edu.cn/portal2017/')

    for i in range(3):
        driver.get(
            f'{iaaaUrl}?appID=portal2017&appName={appName}&redirectUrl={redirectUrl}'
        )
        print('门户登陆中...')
        driver.find_element_by_id('user_name').send_keys(userName)
        time.sleep(0.1)
        driver.find_element_by_id('password').send_keys(password)
        time.sleep(0.1)
        driver.find_element_by_id('logon_button').click()
        try:
            WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.ID, 'all')))
            print('门户登录成功！')
            break
        except:
            print('Retrying...')
        if i == 2:
            raise Exception('门户登录失败')


def go_to_application_out(driver):
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(0.5)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    driver.find_element_by_class_name('el-card__body').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))


def go_to_application_in(driver):
    driver.back()
    driver.back()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    driver.find_element_by_class_name('el-card__body').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))


def select_in_out(driver, way):
    driver.find_element_by_class_name('el-select').click()
    time.sleep(0.1)
    driver.find_element_by_xpath(f'//li/span[text()="{way}"]').click()


def select_campus(driver, campus):
    driver.find_elements_by_class_name('el-select')[1].click()
    time.sleep(0.1)
    driver.find_element_by_xpath(f'//li/span[text()="{campus}"]').click()


def select_destination(driver, destination):
    driver.find_elements_by_class_name('el-select')[2].click()
    time.sleep(0.1)
    driver.find_element_by_xpath(f'//li/span[text()="{destination}"]').click()


def select_district(driver, district):
    driver.find_elements_by_class_name('el-select')[3].click()
    time.sleep(0.1)
    driver.find_element_by_xpath(f'//li/span[text()="{district}"]').click()


def write_reason(driver, reason):
    driver.find_element_by_class_name('el-textarea__inner').send_keys(
        f'{reason}')
    time.sleep(0.1)


def write_track(driver, track):
    driver.find_elements_by_class_name('el-textarea__inner')[1].send_keys(
        f'{track}')
    time.sleep(0.1)


def write_street(driver, street):
    driver.find_elements_by_class_name('el-textarea__inner')[1].send_keys(
        f'{street}')
    time.sleep(0.1)


def click_check(driver):
    driver.find_element_by_class_name('el-checkbox__label').click()
    time.sleep(0.1)


def click_inPeking(driver):
    driver.find_element_by_class_name('el-radio__inner').click()
    time.sleep(0.1)


def submit(driver):
    driver.find_element_by_xpath('//button/span[contains(text(),"保存")]').click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, '(//button/span[contains(text(),"提交")])[3]')))
    driver.find_element_by_xpath(
        '(//button/span[contains(text(),"提交")])[3]').click()
    time.sleep(0.1)


def screen_capture(driver, path):
    driver.back()
    driver.back()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    driver.find_elements_by_class_name('el-card__body')[1].click()
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//button/span[contains(text(),"加载更多")]')))
    driver.maximize_window()
    time.sleep(0.1)
    driver.save_screenshot(path + 'result.png')
    print('备案历史截图已保存')


def fill_out(driver, campus, reason, destination, track):
    print('开始填报出校备案')

    print('选择出校/入校    ', end='')
    select_in_out(driver, '出校')
    print('Done')

    print('选择校区    ', end='')
    select_campus(driver, campus)
    print('Done')

    print('填写出入校事由    ', end='')
    write_reason(driver, reason)
    print('Done')

    print('选择出校目的地    ', end='')
    select_destination(driver, destination)
    print('Done')

    print('填写出校行动轨迹    ', end='')
    write_track(driver, track)
    print('Done')

    click_check(driver)
    submit(driver)

    print('出校备案填报完毕！')


def fill_in(driver, campus, reason, habitation, district, street):
    print('开始填报入校备案')

    print('选择出校/入校    ', end='')
    select_in_out(driver, '入校')
    print('Done')

    print('填写出入校事由    ', end='')
    write_reason(driver, reason)
    print('Done')

    if habitation != '北京':
        raise Exception('暂不支持京外入校备案，请手动填写')

    print('选择居住地所在区    ', end='')
    select_district(driver, district)
    print('Done')

    print('填写居住地所在街道    ', end='')
    write_street(driver, street)
    print('Done')

    click_inPeking(driver)
    click_check(driver)
    submit(driver)

    print('入校备案填报完毕！')


def run(driver, userName, password, campus, reason, destination, track,
        habitation, district, street, capture, path):
    login(driver, userName, password)
    print('=================================')

    go_to_application_out(driver)
    fill_out(driver, campus, reason, destination, track)
    print('=================================')

    go_to_application_in(driver)
    fill_in(driver, campus, reason, habitation, district, street)
    if capture == True:
        print('=================================')
        screen_capture(driver, path)
    print('=================================')
    print('可以愉快的玩耍啦！')


if __name__ == '__main__':
    pass
