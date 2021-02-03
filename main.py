import requests as req
import json

# http首部信息
HEADER = {
    'Host':'stuhealth.jnu.edu.cn',
    'Content-Type':'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Accept-Encoding':'gzip',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Connection':'keep-alive',
    'Origin':'https://stuhealth.jnu.edu.cn',
    'Referer':'https://stuhealth.jnu.edu.cn/'
}

# 自动打卡函数run
def run(log_params):
    # Playload 只能用json格式传递
    log_params = json.dumps(log_params)
    
    # 获取 jnuid 和 idtype 这个两个参数信息
    r = req.post(
        'https://stuhealth.jnu.edu.cn/api/user/login',
        data=log_params,
        headers=HEADER
    )
    # 这里返回一个xhr类型文件，可以解析成json格式
    message = json.loads(r.content)
    
    # 若已打卡，则直接返回
    print(message['meta']['msg'])
    if message['meta']['msg'] == '登录成功，今天已填写':
        return 'main.py: 你今天打过卡啦！'
    elif message['meta']['success'] == False:
        return 'main.py: 请检查你的抓包信息是否有误！'
    
    # 获取 jnuid 和 idtype 
    jnuid = message['data']['jnuid']
    idtype = message['data']['idtype']

    # post stuinfo需要它们
    info_params = {
        'idType': idtype,
        'jnuid': jnuid
    }
    r = req.post(
        'https://stuhealth.jnu.edu.cn/api/user/stuinfo',
        data=json.dumps(info_params),
        headers=HEADER
    )
    message = json.loads(r.content)

    # 学生姓名（你的
    name = message['data']['xm']

    # 构造打卡信息并上传
    # message['data']['mainTable']有你上一次打卡的信息
    # 可以利用它快速构造正确的信息
    mainData = message['data']['mainTable']
    health_params = {
        "mainTable":{
            "wayStart":mainData['wayStart'],
            "arriveTime":mainData['arriveTime'],
            "way2Start":mainData['way2Start'],
            "language":mainData['language'],
            "declareTime":message['meta']['timestamp'].split(' ')[0],
            "personNo":mainData['personNo'],
            "personName":message['data']['xm'],
            "sex":message['data']['xbm'],
            "professionName":message['data']['zy'],
            "collegeName":message['data']['yxsmc'],
            "phoneArea":mainData['phoneArea'],
            "phone":mainData['phone'],
            "assistantName":mainData['assistantName'],
            "assistantNo":mainData['assistantNo'],
            "className":mainData['className'],
            "linkman":mainData['linkman'],
            "linkmanPhoneArea":mainData['linkmanPhoneArea'],
            "linkmanPhone":mainData['linkmanPhone'],
            "personHealth":mainData['personHealth'],
            "temperature":mainData['temperature'],
            "personHealth2":mainData['personHealth2'],
            "leaveState":mainData['leaveState'],
            "leaveHubei":mainData['leaveHubei'],
            "wayType1":mainData['wayType1'],
            "wayType2":mainData['wayType2'],
            "wayType3":mainData['wayType3'],
            "wayType5":mainData['wayType5'],
            "wayType6":mainData['wayType6'],
            "wayTypeOther":mainData['wayTypeOther'],
            "wayNo":mainData['wayNo'],
            "currentArea":mainData['currentArea'],
            "inChina":mainData['inChina'],
            "personC1id":mainData['personC1id'],
            "personC1":mainData['personC1'],
            "personC2id":mainData['personC2id'],
            "personC2":mainData['personC2'],
            "personC3id":mainData['personC3id'],
            "personC3":mainData['personC3'],
            "personC4":mainData['personC4'],
            "otherC4":mainData['otherC4'],
            "isPass14C1":mainData['isPass14C1'],
            "isPass14C2":mainData['isPass14C2'],
            "isPass14C3":mainData['isPass14C3']
        },
        "jnuid":jnuid
    }

    r = req.post(
        'https://stuhealth.jnu.edu.cn/api/write/main',
        data=json.dumps(health_params),
        headers=HEADER
    )
    message = json.loads(r.content)
    return 'main.py: ' + message['meta']['timestamp'] + '\n' + name + '，打卡成功！！'

if __name__ == "__main__":
    # 手动抓包(Chrome开发者模式 F12)
    # 在stuhealth.jnu.edu.cn下，打开开发者模式，选择Network
    # 登陆后，选择login这个xhr类型的文件，底下有postData这行，复制过来就好
    # password是加密后的密码，由于未知加密方式，因此不能构造
    # 请放心使用

    argv = {
        'password': '加密后的密码',
        'username': '你的学号'
    }
    print(run(argv))

