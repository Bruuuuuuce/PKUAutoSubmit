# -*- coding: utf-8
import env_check
from configparser import ConfigParser
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from func import *
import warnings
import sys
import os
import re
warnings.filterwarnings('ignore')


def sys_path(browser):
    path = f'./{browser}/bin/'
    if sys.platform.startswith('win'):
        return path + f'{browser}.exe'
    elif sys.platform.startswith('linux'):
        return path + f'{browser}-linux'
    elif sys.platform.startswith('darwin'):
        return path + f'{browser}'
    else:
        raise Exception('暂不支持该系统')


def go(config):
    conf = ConfigParser()
    conf.read(config, encoding='utf8')

    userName, password = dict(conf['login']).values()
    campus, reason, detail = dict(conf['common']).values()
    destination, track = dict(conf['out']).values()
    habitation, district, street = dict(conf['in']).values()
    capture = conf.getboolean('capture', '是否需要备案历史截图')
    path = conf['capture']['截图保存路径']
    wechat = conf.getboolean('wechat', '是否需要微信通知')
    sckey = conf['wechat']['SCKEY']

    run(driver_pjs, userName, password, campus, reason, detail, destination, track,
        habitation, district, street, capture, path, wechat, sckey)


if __name__ == '__main__':

    # driver_pjs = webdriver.PhantomJS(executable_path=sys_path(browser="phantomjs"))

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver_pjs = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            options=chrome_options,
            service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    print('Driver Launched\n')

    lst_conf = sorted([
        fileName for fileName in os.listdir()
        if re.match(r'^config[0-9][0-9]*\.ini$', fileName)
    ],
        key=lambda x: int(re.findall(r'[0-9]+', x)[0]))

    print(f'读取到{len(lst_conf)+1}份配置文件\n')
    print('||第1个学生备案||')
    go('config.ini')

    if lst_conf:
        for num, config in enumerate(lst_conf):
            print(f'||第{num+2}个学生备案||')
            go(config)

    driver_pjs.quit()
