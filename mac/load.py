import json

data = {
    # 手动抓包
    # 在stuhealth.jnu.edu.cn下，打开开发者模式，选择Network
    # 登陆后，选择login这个xhr文件，底下有postData，复制过来就好
    "username": "",
    "password": ""
}

with open('./data/password.json','w') as f:
    json.dump(data,f)