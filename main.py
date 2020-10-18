# -*- coding: utf-8
import env_check
from configparser import ConfigParser
from func import *
import warnings
import os
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    conf = ConfigParser()
    conf.read('config.ini', encoding='utf8')

    userName, password = dict(conf['login']).values()
    campus, reason = dict(conf['common']).values()
    destination, track = dict(conf['out']).values()
    habitation, district, street = dict(conf['in']).values()
    capture = conf.getboolean('capture', '是否需要备案历史截图')
    path = conf['capture']['截图保存路径']
    wechat = conf.getboolean('wechat', '是否需要微信通知')
    sckey = conf['wechat']['SCKEY']

    print('Driver Launching...')
    
    if os.name == "nt":
        driver_pjs = webdriver.PhantomJS(
            executable_path='./phantomjs/bin/phantomjs.exe')
    else:
        driver_pjs = webdriver.PhantomJS(
            executable_path='./phantomjs/bin/phantomjs')
    run(driver_pjs, userName, password, campus, reason, destination, track,
        habitation, district, street, capture, path, wechat, sckey)
    driver_pjs.quit()
