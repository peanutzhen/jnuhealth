from daemon import Daemon
from time import sleep
import requests as req
import json
import datetime


## 打卡成员列表
# 手动抓包(Chrome开发者模式 F12)
# 在stuhealth.jnu.edu.cn下，打开开发者模式，选择Network
# 登陆后，选择login这个xhr类型的文件，底下有postData这行，复制过来就好
# password是加密后的密码，由于未知加密方式，因此不能构造
# 请放心使用
attend_list = [
    {
        'password': '加密后的密码',
        'username': '你的学号'
    }
]

# http首部信息
HEADER = {
    'Host': 'stuhealth.jnu.edu.cn',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.138 Safari/537.36',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://stuhealth.jnu.edu.cn',
    'Referer': 'https://stuhealth.jnu.edu.cn/'
}


class Server(Daemon):
    def run(self):
        while True:
            for student in attend_list:
                # 最大重试次数 10
                for attempt in range(10):
                    try:
                        self.attend(student)
                    except:
                        sleep(5)
                        continue
                    else:
                        break

            t = datetime.datetime.today()
            # 每晚凌晨2点自动打卡 你可以设置你想自动打卡的时间
            future = datetime.datetime(t.year, t.month, t.day, 2, 0)
            if t.hour >= 2:
                future += datetime.timedelta(days=1)
            sleep((future - t).total_seconds())

    # 自动打卡函数run
    def attend(self, log_params):
        # 获取 jnuid 和 idtype 这个两个参数信息
        r = req.post(
            'https://stuhealth.jnu.edu.cn/api/user/login',
            data=json.dumps(log_params),  # Playload 只能用json格式传递
            headers=HEADER
        )
        message = json.loads(r.content)  # 这里返回一个xhr类型文件，可以解析成json格式

        # 若已打卡，则直接返回
        if message['meta']['msg'] == '登录成功，今天已填写':
            print('main.py: %s今天打过卡啦！' % (log_params.get('username')))
            return
        elif message['meta']['msg'] == '登录成功，今天未填写':
            print('main.py: %s正在打卡...' % (log_params.get('username')))
        elif message['meta']['success'] == False:
            print(message['meta']['msg'] + 'main.py: 请检查你的log_params是否有误！')
            return

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
        mainTable = message['data']['mainTable']
        mainTable["declareTime"] = message['meta']['timestamp'].split(' ')[0]
        mainTable["personName"] = message['data']['xm'],
        mainTable["sex"] = message['data']['xbm'],
        mainTable["professionName"] = message['data']['zy'],
        mainTable["collegeName"] = message['data']['yxsmc'],

        secondTable = message['data']['secondTable']
        payload = {
            "mainTable": mainTable,
            "secondTable": secondTable,
            "jnuid": jnuid
        }

        r = req.post(
            'https://stuhealth.jnu.edu.cn/api/write/main',
            data=json.dumps(payload),
            headers=HEADER
        )
        message = json.loads(r.content)
        if message["meta"]["success"] == True:
            print('main.py: ' + message['meta']['timestamp'] + name + '，打卡成功！！')
        else:
            print(f'main.py: post failed, due to {message["meta"]}')


if __name__ == "__main__":
    server = Server(
        pidfile='pidfile',
        umask=0,
        stdout='attend.log',
        stderr='error.log'
    )
    server.start()
