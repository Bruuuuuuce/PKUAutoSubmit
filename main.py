from selenium.webdriver import Firefox, Chrome, PhantomJS
from argparse import ArgumentParser
from func import run
import copy
import sys
import os


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--username', '-u', type=str, help='username, eg. 2000010000')
    parser.add_argument('--password', '-p', type=str, help='password, eg. here_is_my_password')
    parser.add_argument('--campus', type=str, help='所在校区, 燕园、万柳、畅春园、圆明园、中关新园')
    parser.add_argument('--reason', type=str, help='出校原因, eg. 吃饭')
    parser.add_argument('--destination', type=str, help='出校目的地, eg. 北京')
    parser.add_argument('--track', type=str, help='出校轨迹, eg. 畅春园食堂')
    parser.add_argument('--habitation', type=str, help='入校前居住地, eg. 北京')
    parser.add_argument('--district', type=str, help='入校前居住所在区, eg. 海淀区')
    parser.add_argument('--street', type=str, help='入校前居住所在街道, eg. 燕园街道')
    args = parser.parse_args()

    args_public = copy.deepcopy(args)
    args_public.password = 'xxxxxxxx'
    print('Arguments: {}'.format(args_public))
    print('Driver Launching...')

    # driver = Firefox()
    # driver = Chrome()

    if sys.platform == 'darwin':    # macOS
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-darwin')
    elif sys.platform == 'linux':   # linux
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-linux-x86_64')
    else:                           # windows
        phantomjs_path = os.path.join('phantomjs', 'phantomjs-windows.exe')
    
    driver = PhantomJS(executable_path=phantomjs_path)

    run(
        driver,
        args.username,
        args.password,
        args.campus,
        args.reason,
        args.destination,
        args.track,
        args.habitation,
        args.district,
        args.street
    )
    
    driver.close()
