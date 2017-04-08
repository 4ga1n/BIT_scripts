#coding:utf-8
import ConfigParser
import os
import time

import requests
from plyer import notification

from ping import verbose_ping
# https://github.com/samuel/python-ping/blob/master/ping.py


def new_ping(hostname):
    response = os.system('ping ' + hostname + ' -w 1000')
    if response == 0:
        return True
    else:
        return False

def load_config():
    cf = ConfigParser.SafeConfigParser()


    if os.path.exists("config.ini"):
        pass
    else:
        print "no config file, creat file automatically"
        config_str = """[account]
username=aaaa
password=bbbb
;change aaaa,bbbb to your account and password。
;出现问题请先在后台杀掉程序后重新启动程序。
;有问题或报bug请发邮件到zxacd@qq.com
;或上github上pull requests。https://github.com/4ga1n/BIT_scripts
"""
        with open('config.ini', 'w') as file_:
            file_.write(config_str)

        os.system('notepad.exe config.ini')

    cf.read("config.ini")

    return cf.get("account", "username"), cf.get("account", "password")


def test_the_internet_connection(testcount):
    response = verbose_ping('www.baidu.com', count=testcount)
    if 'get ping' in response:
        print '[2]the Internet is OK'
        return True
    else:
        print '[2]the Internet is disconnected'
        return False

def test_school_internet_connection(testcount):
    response = verbose_ping('10.0.0.55', count=testcount)
    if 'get ping' in response:
        print '[1]school internet is OK'
        return True
    else:
        print '[1]school internet is disconnected'
        return False

def wait_school_internet(testcount, timewait):
    while True:
        has_internet = test_school_internet_connection(testcount)
        if not has_internet:
            print '[1.5 school net error]'
            time.sleep(timewait)
        else:
            return

def connection_loop(testcount, timewait):
    while True:
        has_the_internet = test_the_internet_connection(testcount)
        if has_the_internet:
            print '[2.5 internet ok]'
            time.sleep(timewait)
        else:
            return
def main():
    username, password = load_config()
    print "use SafeConfigParser() read"
    print "username = ", username
    print "password = ", password
    while True:
        # phase 2 test connection
        the_internet = test_the_internet_connection(4)
        if the_internet:
            connection_loop(1, 52) #should be (1,60), test use (1,10)
            continue
        # phase 1 test school internet
        school_internet = test_school_internet_connection(2)
        if not school_internet:
            wait_school_internet(1, 10)
        notify_flag_a = False
        notify_flag_b = False

        while True:
            # phase 2 test connection
            the_internet = test_the_internet_connection(4)
            if the_internet:
                connection_loop(1, 52) #should be (1,60), test use (1,10)
            else:
                # phase 3 login
                try:
                    print '[3] geting loginurl'
                    loginurl = requests.get('http://10.0.0.55/ac_detect.php?ac_id=1&').url
                except requests.exceptions.RequestException as e:
                    print e
                    print 'connection error, return to phase 1'
                    break
                try:
                    print '[3] logining'
                    postdata = {'username': username, 'save_me': '0', 'ajax': '1', \
                             'action': 'login', 'password': password, 'ac_id': '1'}
                    response = requests.post(loginurl, data=postdata)
                    if 'login_ok' in response.text:
                        print '[3] login ok'
                    elif 'IP has been online' in response.text:
                        print '[3] logined IP has online'
                        the_internet = True
                    elif 'Password is error' in response.text:
                        print '[3] password is error'
                        # 重新读取账户密码
                        username, password = load_config()
                        print username, password
                        if not notify_flag_a:
                            notification.notify(
                                title='bit_auto_connect',
                                message='password or account wrong',
                                app_name='bit_auto_connect',
                            )
                            notify_flag_a = True
                    elif 'E2616' in response.text:
                        print '[3] in debt'
                        if not notify_flag_b:
                            notification.notify(
                                title='bit_auto_connect',
                                message='in debt',
                                app_name='bit_auto_connect',
                            )
                            notify_flag_b = True
                    else:
                        print '[3] unknow cases'
                        print response.text
                    print '[3.5] heading to phase 2'
                except requests.exceptions.RequestException as e:
                    print e
                    print 'connection error, return to phase 1'
                    break


if __name__ == '__main__':
    main()
