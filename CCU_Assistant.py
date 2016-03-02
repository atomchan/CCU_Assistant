# -*- coding: utf-8 -*-
import urllib2
import cookielib
import urllib
from bs4 import BeautifulSoup
import re
import os
import platform
import ConfigParser

def GetUsers():
        '''Get usres info from config.ini
        if not exist, return {}
        '''

        cf = ConfigParser.ConfigParser()
        if 'config.ini' in os.listdir(os.getcwd()):
                cf.read('config.ini')
        else:
                return {}
        secs = cf.sections()
        general = dict(cf.items('General'))
        users = dict(cf.items('Users'))
        general.update(users)
        return general

def WriteUsers(num, data):
        '''Write user's information to config.ini
        asume:
        num likes: 3
        data likes: {'user3':'012345678', 'pass3':'impassword'}
        '''
        cf = ConfigParser.ConfigParser()
        if 'config.ini' in os.listdir(os.getcwd()):
                with open('config.ini', 'r+') as f:
                        cf.read('config.ini')
                        cf.set('General', 'users', num)
                        cf.set('Users', 'user'+str(num), data['user'+str(num)])
                        cf.set('Users', 'pass'+str(num), data['pass'+str(num)])
                        cf.write(f)
        else:
                with open('config.ini', 'w') as f:
                        cf.read('config.ini')
                        cf.add_section('General')
                        cf.set('General', 'users', num)
                        cf.add_section('Users')
                        cf.set('Users', 'user'+str(num), data['user'+str(num)])
                        cf.set('Users', 'pass'+str(num), data['pass'+str(num)])
                        cf.write(f)

def WelcomeText():
        print('欢迎使用长大助手 v1.0.0版')
        print('*'*40)
        print('本助手目前功能只有一键自动查成绩（可自动解决教务管理系统当前登录人数过多的问题哦)')
        print('前人栽树,后人乘凉.')
        print('代码继承自 Mathematrix (mathematrix.sinaapp.com)')
        print('*'*40)
        print('目前已知bugs:')
        print('1. 有时会因为莫名无法查询到成绩，大家在确保信息正确的情况下可尝试多运行几次')
        print('2. 用户信息会明文保存在程序运行文件夹内的config.ini内，尚拿不定主意究竟要加密保存还是明文保存 另外现在如果想修改已保存信息 可直接打开这个文件修改')
        print('本项目开源在github 项目主页: https://github.com/sintonwong/CCU_Assistant')
        print('程序介绍及更新网址: http://sintonblog.win ')
        print('*'*70)
        print('\n')

WelcomeText()
data = GetUsers()
if len(data) == 0:
        print('本地暂无用户数据保存，请输入新数据: ')
        username = raw_input('输入你的学号然后按下回车键: \n')
        password = raw_input('输入你的教务处密码然后按下回车键: \n')
        data['users'] = 1
        data['user1'] = username
        data['pass1'] = password
        WriteUsers(1, data)
else:
        print('已有 {0} 个用户的数据，选择其中一个来查询（输入后按下回车键）: '.format(int(data['users'])))
        for i in range(1, int(data['users']) + 1):
                print('{0}. {1}'.format(i, data['user' + str(i)]))
        print('{0}. 输入一份新的数据'.format(i + 1, ))
        choice = raw_input('输入 \'1\' 或者别的数字（输入后按下回车键）: ')
        if choice == str(i + 1):
                username = raw_input('输入你的学号然后按下回车键: \n')
                password = raw_input('输入你的教务处密码然后按下回车键: \n')
                data['users'] = i + 1
                data['user' + str(i + 1)] = username
                data['pass' + str(i + 1)] = password
                WriteUsers(i + 1, data)
        else:
                username = data['user' + str(choice)]
                password = data['pass' + str(choice)]

login = 'http://www.cdjwc.com/jiaowu/Login.aspx'
jw = 'http://www.cdjwc.com/jiaowu/JWXS/Default.aspx'
grates = 'http://www.cdjwc.com/jiaowu/JWXS/cjcx/jwxs_cjcx_like.aspx'

req = urllib.urlopen(login)
content = req.read()
req.close()

soup = BeautifulSoup(content, "html.parser")

foundVIEWSTATE = re.search('<input\s+?type="hidden"\s+?name="__VIEWSTATE"\s+?id="__VIEWSTATE"\s+?value="(?P<value>.+?)"\s+?/>',content)
if(foundVIEWSTATE):
        VIEWSTATE = foundVIEWSTATE.group("value")
 #       print VIEWSTATE

foundEVENTVALIDATION = re.search('<input\s+?type="hidden"\s+?name="__EVENTVALIDATION"\s+?id="__EVENTVALIDATION"\s+?value="(?P<value>.+?)"\s+?/>', content)
if(foundEVENTVALIDATION):
        EVENTVALIDATION = foundEVENTVALIDATION.group("value")
 #       print EVENTVALIDATION

data = {
        '__VIEWSTATE' : VIEWSTATE,
        '__EVENTVALIDATION' : EVENTVALIDATION,
        'Account' : username,
        'PWD' : password,
        'cmdok' : ''
}

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)
urllib2.install_opener(opener)

print('正在登录...')
login = urllib2.urlopen(login,urllib.urlencode(data))
c = urllib2.urlopen(grates)
print('正在从教务处获得数据...')


with open('output.html', 'w') as f:
    header = r'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    data = header + "<h3 align=center>欢迎使用长大助手 v1.0.0</h3>" + c.read().decode('gbk').encode('utf-8') + "\n"
    f.write(data)
    f.flush()
if platform.system() == 'Windows':
    print('正在打开成绩查询页面...')
    os.system('output.html')
elif platform.system() == 'Linux':
    os.system('gnome-open output.html')
elif platform.system() == 'Darwin':
	print ('正在打开成绩查询页面...若无法打开请手动打开运行目录下的"output.html"')
	os.system('open /Applications/Safari.app output.html')

opener.close()
login.close()
c.close()