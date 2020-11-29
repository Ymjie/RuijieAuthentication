# coding=utf-8
import requests
import json
import time
import prettytable as pt


def post(url, data):
    r = requests.post(url, data)
    data = json.loads(r.content)
    return data


def login(uid, password):
    url = 'http://172.20.255.1:9090/eportal/InterFace.do?method=login'
    data = {
        'userId': uid,
        'password': password,
        'service': 'internet',
        'queryString': '&t=wireless-v2-plain&nasip=10.191.0.2',
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': 'false'
    }
    return post(url, data)


def getInfo(userindex):
    url = 'http://172.20.255.1:9090/eportal/InterFace.do?method=getOnlineUserInfo'
    data = {'userIndex': userindex}
    data = post(url, data)
    return data


def isLogin():
    data = login(0, 0)
    # print(data)
    if data['result'] == 'success':
        return data
    return False


def logout(userindex):
    url = 'http://172.20.255.1:9090/eportal/InterFace.do?method=logout'
    data = {'userIndex': userindex}
    data = post(url, data)
    return data


def reFreshUserData(userindex):
    errnum = 0
    while True:
        data = getInfo(userindex)
        # print(data['maxLeavingTime'])
        if data['maxLeavingTime'] != None:
            print('获取到完整信息！')
            break
        print('刷新，认证服务器并未返回完整信息，请耐心等待10S！')
        time.sleep(10)
        errnum = errnum+1
        if errnum > 10:
            print('长时间无完整信息，这号有点问题！等会再试试吧，年轻人。')
            return False
    return data


def echoData(userdata):
    akey = {
        'maxLeavingTime': '最大在线时长',
        'userName': '用户名',
        'userId': 'UID',
        'userIp': '登录IP',
        'service': '服务',
        'userGroup': '用户组',
        'loginType': '登录方式',
        'accountFee': '账户余额',
        'userPackage': '用户套餐',
        'welcomeTip': '欢迎Tip',
        'isCloseWinAllowed': '是否允许局域网网络分享',
        'checkUserLogout': '最大在线设备数量',
        'isAutoLogin': '是否自动登录',
        'mabInfoMaxCount': '最大无感认证设备数量',
        # 'mabInfo':'当前无感认证信息'
    }
    for key in akey:
        print('{key} : {val}'.format(key=akey[key], val=userdata[key]))
    return


def echoMacMenu(macMenu, userdata):
    macData = userdata['mabInfo']
    macData = json.loads(macData)
    tb = pt.PrettyTable()
    name = ["createHost", "createTime", "deviceType",
            "showMacExpireTime", 'systemType', 'userMac']
    row = []
    for mac in macData:
        for key in name:
            row.append(mac[key])
        tb.add_row(row)
        row = []
    tb.field_names = name
    print(tb)

    echoMenu(macMenu)
    id = int(input('输入ID:'))
    if id == 0:
        print('开发中')
    if id == 1:
        print('开发中')

    return


mainMenu = {
    'title': '主菜单',
    'tip': '输入序号并回车',
    'list': [
        '基础信息',
        '无感认证信息/设置',
        '注销退出账号',
        '退出'
    ]
}
macMenu = {
    'title': 'Mac',
    'tip': '输入序号并回车',
    'list': [
        '无感认证本机Mac',
        '注销已注册Mac'
    ]
}


def echoMenu(menu):
    print('************'+menu['title']+'************')
    print('Tip:'+menu['tip'])
    id = 0
    menulist = menu['list']  # 防止list乱序
    for mlist in menulist:
        print("   {id}.{one}".format(id=id, one=mlist))
        id = id + 1
    print('**************************************')
    return


def fun_mainMenu(menu, userdata):
    islog = isLogin()
    if islog == False:
        print('账号已经退出')
        exit()
    echoMenu(menu)
    id = input('输入ID:')
    id = int(id)
    if id == 0:
        echoData(userdata)
    if id == 1:
        echoMacMenu(macMenu, userdata)
    if id == 3:
        exit()
    if id == 2:
        err = logout(userdata['userIndex'])
        print(err)
    return


print('---校园网 认证/设置 脚本---')
print("检查是否登录")
islog = isLogin()
if islog != False:
    logdata = islog
    print('检测到你已经登录校园网')
while islog == False:
    uid = input('输入学号/工号：')
    password = input('输入密码：')
    logdata = login(uid, password)
    print(logdata['message'])
    if logdata['result'] != 'success':
        if logdata['validCodeUrl'] != '':
            print('达到最大尝试次数，出现验证码，脚本将退出，请稍后再试！')
            exit()
    else:
        print('登录成功')
        islog = True
userdata = reFreshUserData(logdata['userIndex'])
if userdata == False:
    print('按任意键退出')
    input()
    exit()
while True:
    fun_mainMenu(mainMenu, userdata)
