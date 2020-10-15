from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox, Chrome, PhantomJS
from selenium import webdriver
from argparse import ArgumentParser
from urllib.parse import quote
import time
import copy
import sys
import os

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

my_sender = '1692484707@qq.com'  # 发件人邮箱账号
my_pass = 'fujkixpkjiyhcaji'  # 发件人邮箱密码
my_user = 'kevin.z2001@hotmail.com'  # 收件人邮箱账号


def mail():
    ret = True
    try:
        cur_time = time.strftime("%d/%m/%Y")
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = Header('PKU-AutoSubmit', 'utf-8')
        msgRoot['To'] = Header('student', 'utf-8')
        subject = cur_time + ' 报备成功 '
        msgRoot['Subject'] = Header(subject, 'utf-8')

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        mail_msg = """
        <p>自动报备成功！</p>
        <p>截图：</p>
        <p><img src="cid:image1"></p>
        """
        msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        # 指定图片为当前目录
        fp = open('result.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()

        # 定义图片 ID，在 HTML 文本中引用
        msgImage.add_header('Content-ID', '<image1>')
        msgRoot.attach(msgImage)
        
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user, ], msgRoot.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret

TIMEOUT = 10
TIMESLP = .5

def login(driver, username, password, failed=0):
    if failed == 3:
        raise Exception('门户登录失败')

    iaaaUrl = 'https://iaaa.pku.edu.cn/iaaa/oauth.jsp'
    appName = quote('北京大学校内信息门户新版')
    redirectUrl = 'https://portal.pku.edu.cn/portal2017/ssoLogin.do'
    driver.get('https://portal.pku.edu.cn/portal2017/')
    driver.get(
        f'{iaaaUrl}?appID=portal2017&appName={appName}&redirectUrl={redirectUrl}'
    )

    print('门户登陆中...')
    driver.find_element_by_id('user_name').send_keys(username)
    time.sleep(TIMESLP)
    driver.find_element_by_id('password').send_keys(password)
    time.sleep(TIMESLP)
    driver.find_element_by_id('logon_button').click()

    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.LINK_TEXT, '我知道了')))
    except:
        pass
    else:
        driver.find_element_by_link_text('我知道了').click()

    try:
        WebDriverWait(driver, TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, 'all')))
    except:
        login(driver, username, password, failed + 1)
    else:
        print('门户登录成功！')


def go_to_application_out(driver):
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(TIMESLP)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    time.sleep(TIMESLP)
    driver.find_element_by_class_name('el-card__body').click()
    time.sleep(TIMESLP)
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-input__inner')))


def go_to_application_in(driver):
    driver.get('https://portal.pku.edu.cn/portal2017/#/bizCenter')
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'all')))
    driver.find_element_by_id('all').click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, 'tag_s_stuCampusExEnReq')))
    driver.find_element_by_id('tag_s_stuCampusExEnReq').click()
    time.sleep(TIMESLP)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-card__body')))
    time.sleep(TIMESLP)
    driver.find_element_by_class_name('el-card__body').click()
    time.sleep(TIMESLP)
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'el-select')))


def select_in_out(driver, way):
    driver.find_element_by_class_name('el-select').click()
    time.sleep(TIMESLP)
    driver.find_element_by_xpath(f'//li/span[text()="{way}"]').click()


def select_campus(driver, campus):
    driver.find_elements_by_class_name('el-select')[1].click()
    time.sleep(TIMESLP)
    driver.find_element_by_xpath(f'//li/span[text()="{campus}"]').click()


def select_destination(driver, destination):
    driver.find_elements_by_class_name('el-select')[2].click()
    time.sleep(TIMESLP)
    driver.find_element_by_xpath(f'//li/span[text()="{destination}"]').click()


def select_district(driver, district):
    driver.find_elements_by_class_name('el-select')[3].click()
    time.sleep(TIMESLP)
    driver.find_element_by_xpath(f'//li/span[text()="{district}"]').click()


def write_reason(driver, reason):
    driver.find_element_by_class_name('el-textarea__inner').send_keys(
        f'{reason}')
    time.sleep(TIMESLP)


def write_track(driver, track):
    driver.find_elements_by_class_name('el-textarea__inner')[1].send_keys(
        f'{track}')
    time.sleep(TIMESLP)


def write_street(driver, street):
    driver.find_elements_by_class_name('el-textarea__inner')[1].send_keys(
        f'{street}')
    time.sleep(TIMESLP)


def click_check(driver):
    driver.find_element_by_class_name('el-checkbox__label').click()
    time.sleep(TIMESLP)


def click_inPeking(driver):
    driver.find_element_by_class_name('el-radio__inner').click()
    time.sleep(TIMESLP)


def submit(driver):
    driver.find_element_by_xpath(
        '//button/span[contains(text(),"保存")]').click()
    WebDriverWait(driver, TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, '(//button/span[contains(text(),"提交")])[3]')))
    driver.find_element_by_xpath(
        '(//button/span[contains(text(),"提交")])[3]').click()
    time.sleep(TIMESLP)
    
def screen_capture(driver):
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
    driver.save_screenshot('result.png')
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


def run(driver, username, password, campus, reason, destination, track,
        habitation, district, street):
    login(driver, username, password)
    print('=================================')

    go_to_application_out(driver)
    fill_out(driver, campus, reason, destination, track)
    print('=================================')

    go_to_application_in(driver)
    fill_in(driver, campus, reason, habitation, district, street)
    print('=================================')
    
    screen_capture(driver)
    print('=================================')
     
    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")
        
    print('可以愉快的玩耍啦！')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--username', '-u', type=str, help='用户名')
    parser.add_argument('--password', '-p', type=str, help='密码')
    parser.add_argument('--campus', type=str, help='所在校区, 燕园、万柳、畅春园、圆明园、中关新园', default='燕园')
    parser.add_argument('--reason', type=str, help='出校原因, eg. 吃饭', default='上课/回宿舍')
    parser.add_argument('--destination', type=str, help='出校目的地, eg. 北京', default='北京')
    parser.add_argument('--track', type=str, help='出校轨迹, eg. 畅春园食堂', default='东南门-理教-东南门')
    parser.add_argument('--habitation', type=str, help='入校前居住地, eg. 北京', default='北京')
    parser.add_argument('--district', type=str, help='入校前居住所在区, eg. 海淀区', default='海淀区')
    parser.add_argument('--street', type=str, help='入校前居住所在街道, eg. 燕园街道', default='燕园街道')
    args = parser.parse_args()

    args_public = copy.deepcopy(args)
    args_public.password = 'xxxxxxxx'
    print('Arguments: {}'.format(args_public))
    print('Driver Launching...')

    # driver = Firefox()
    # driver = Chrome()

    if sys.platform == 'darwin':  # macOS
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-darwin')
    elif sys.platform == 'linux':  # linux
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-linux-x86_64')
    else:  # windows
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-windows.exe')

    driver = PhantomJS(executable_path=phantomjs_path)

    run(driver, args.username, args.password, args.campus, args.reason,
        args.destination, args.track, args.habitation, args.district,
        args.street)

    driver.close()
