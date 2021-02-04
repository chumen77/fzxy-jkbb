'''
@author chumen77
@desc 本脚本是用于翻转校园的每日健康报备
@date 2020/01/28
'''

# encoding: utf-8
import requests
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from Crypto import Random
import base64
import hashlib
import json
import urllib
import time
requests.packages.urllib3.disable_warnings()

debug = 0 #开启或者关闭debug  主要是来显示cookie 密码相关的

#此处填写你的帐号密码
account = ''
password = ''

#此处填写你的相关报备信息 建议这块对着软件当时的报备界面的表单进行填写
homeAddress='' #家的地址 例如：河南+郑州+中牟 其中 "+" 号不要省略。 "省 市" 省略不填写。
homeAddressDetail='' #例如： 大王村
myPhone='' #个人手机号
mecName='' #家长姓名
mecPhone='' #对应家长电话
hujiAddress='' #当前所在地址 例如： 河南+郑州+中牟 其中 "+" 号不要省略。 "省 市" 省略不填写。
addressDetail='' #当前所在详细地址 例如:大王村
address='' #当前所在地址 例如： 河南+郑州+中牟 其中 "+" 号不要省略。 "省 市" 省略不填写。

dormBuild= '' #宿舍所在楼号 例如：湖滨校区10号楼
dormCell='' #宿舍所在的楼层号 例如：6
dormNum='' #宿舍号 例如：628


def main():
    BLOCK_SIZE = 16  # Bytes
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * \
                    chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
    unpad = lambda s: s[:-ord(s[len(s) - 1:])]
    def aesEncrypt(key, data):
        key = key.encode('utf8')
        data = pad(data)
        cipher = AES.new(key, AES.MODE_ECB)
        result = cipher.encrypt(data.encode())
        encodestrs = base64.b64encode(result)
        enctext = encodestrs.decode('utf8')
        if debug:
            print("password : ---->" + enctext)
        return enctext

    def md5vale(key):
        input_name = hashlib.md5()
        input_name.update(key.encode("utf-8"))
        return input_name.hexdigest()

    def encrypt(message, random):
        suffix = 'dlp'
        companyCode = 'youcai'
        nouce = random + '.' + companyCode + '.' + suffix
        keyHash = md5vale(nouce);
        ecdata = aesEncrypt(keyHash,message)
        return ecdata;

    if account == '' or password == '':
        print('请检查你的账号密码是否在代码上方填写~')
        exit()
    print("你的登陆帐号为: " + account)
    gets_session = requests.Session()
    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Cache-Control":"no-cache","Upgrade-Insecure-Requests":"1","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0","Referer":"https://www.schoopia.com/login","Connection":"close","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate","Pragma":"no-cache"}
    response = gets_session.get("https://www.schoopia.com/login", headers=headers,verify=False)
    if response.status_code ==200 :
        print('获取登陆相关messages成功了~')
    else:
        print('获取登陆相关messages失败了~')

    cookies = response.cookies.items()
    cookie = ''
    phpsessid = cookies[0][1]
    acw_tc = cookies[1][1]
    if debug :
        print('acw_tc :---->' + acw_tc)
        print('phpsessid :---->' + phpsessid)


    random_session = requests.Session()
    paramsGet = {"ajax":"true","cmd":"prepare"}
    headers = {"Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0","Connection":"close","Referer":"https://www.schoopia.com/login","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate"}
    cookies = {"acw_tc":"{0}".format(acw_tc),"PHPSESSID":"{0}".format(phpsessid)}
    response = random_session.get("https://www.schoopia.com/login", params=paramsGet, headers=headers, cookies=cookies,verify=False)

    if response.status_code ==200 :
        print('获得random数成功了~')
    else:
        print('获得random数失败了~')


    text = response.text
    jsonobj = json.loads(text)
    random = jsonobj['data']['random']
    init_password = encrypt(password, random)


    login_session = requests.Session()
    paramsPost = {"random":"{0}".format(random),"password":"{0}".format(init_password),"device":"pc","key":"{}".format(account),"ds":"0"}
    headers = {"Origin":"https://www.schoopia.com","Accept":"application/json, text/javascript, */*; q=0.01","X-Requested-With":"XMLHttpRequest","User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0","Connection":"close","Referer":"https://www.schoopia.com/login","Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2","Accept-Encoding":"gzip, deflate","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
    response = login_session.post("https://www.schoopia.com/login", data=paramsPost, headers=headers, cookies=cookies,verify=False)


    if response.status_code == 200 :
        print('提交登陆信息成功了~')
    else:
        print('提交登陆信息失败了~')

    import random
    localtime = time.asctime( time.localtime(time.time()) )
    print("本地时间为 :" + localtime)
    tem_buf = random.uniform(36.1,36.8)
    temperature = format(tem_buf,'.1f')
    print('你今天的体温是:' + str(temperature))


    temperature_session = requests.Session()
    headers = {"Origin":"https://bs.schoopia.com","Accept":"*/*","X-Requested-With":"XMLHttpRequest","BToken":"{0}".format(phpsessid),"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Referer":"https://bs.schoopia.com/wap/health/record","Connection":"close","Accept-Encoding":"gzip, deflate","Accept-Language":"zh-cn","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}
    cookies = {"PHPSESSID":"{0}".format(phpsessid)}
    buf = "homeAddress={0}&homeAddressDetail={1}&myPhone={2}&mecName={3}&mecPhone={4}&hujiAddress={5}&dormBuild={6}&dormCell={7}&dormNum={8}&todayHot={9}&healthType=0&healthTypeStr=&addressDetail={10}&badType=0&backFlag=0&outFlag=0&outForceFlag=0&homeForceFlag=0&homeForceStart=&homeForceEnd=&hospitalType=0&outType=0&outTime=&outAddress=&outBackTime=&outTakeInfo=&outTypeCity=&outTypeCityHomeFlag=0&outTypeHomeCity=&outTypeCityHomeTime=&outTypeCityFlag=0&backSchool=0&backSchoolTime=&agree=1&backSchoolTakeInfo=&homeBadType=0&address={11}&badTypeTime=&outTypeCityCountryTo=&outTypeCityTouch=&outTypeCityCountryTouch=&outTypeHomeCityCountry=&outTypeHomeCityTouch=&outTypeHomeCityTouchCountry=&detail=".format(homeAddress,homeAddressDetail,myPhone,mecName,mecPhone,hujiAddress,dormBuild,dormCell,dormNum,temperature,addressDetail,address)
    rawBody = urllib.parse.quote(buf)
    rawBody = urllib.parse.unquote(rawBody) #python3
    response = temperature_session.post("https://bs.schoopia.com/wap/health/record/save/new", data=rawBody.encode('utf-8'), headers=headers, cookies=cookies,verify=False) #python3

    if response.status_code == 200 :
        print('提交体温状态正常')
    else:
        print('提交体温状态异常,请检查帐号密码和你的报备信息是否按照注释的格式')

    check_session = requests.Session()
    headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","BToken":"{0}".format(phpsessid),"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148","Connection":"keep-aliv","Accept-Language":"zh-cn","Accept-Encoding":"gzip, deflate, br"}
    cookies = {"acw_tc":"{0}".format(acw_tc),"PHPSESSID":"{0}".format(phpsessid)}
    response = check_session.get("https://bs.schoopia.com/wap/health/record/", headers=headers, cookies=cookies,verify=False)


    if response.status_code == 200 :
        print('检验是否报备成功 成功了~')
    else:
        print('检验是否报备成功 失败了~')

    text = response.text
    flag = '您已录入今天的健康信息'

    if(flag in text):
        print('成功了～您已录入今天的健康信息!')
    else :
        print('失败了～您没有录入今天的健康信息!请检查帐号密码和你的报备信息是否按照注释的格式~')


main()
