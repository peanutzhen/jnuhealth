import requests as req
import json

def run():
    # loading password info...
    log_params = None
    try:
        with open("./data/password.json",'r') as f:
            log_params = json.load(f)
    except FileNotFoundError:
        return "Check ./data/password.json is existent? "

    log_params = json.dumps(log_params)
    # Only accept json, cause it is a playload instead of Form data!

    play_load_header = {
        'Host':'stuhealth.jnu.edu.cn',
        'Content-Type':'application/json',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                      AppleWebKit/537.36 (KHTML, like Gecko) \
                      Chrome/81.0.4044.138 Safari/537.36',
        'Accept-Encoding':'gzip',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Type':'application/json',
        'Origin':'https://stuhealth.jnu.edu.cn',
        'Referer':'https://stuhealth.jnu.edu.cn/'
    }


    # This is a step to get jnuid and idtype.
    login = 'https://stuhealth.jnu.edu.cn/api/user/login'
    r = req.post(login,
                 data=log_params,
                 headers=play_load_header)

    # r returns a xhr file, and it can be decoded by json.
    message = json.loads(r.content)

    # These params are what we want!!!!hahahahahah
    jnuid = message['data']['jnuid']
    idtype = message['data']['idtype']

    # Building params...
    info_params ={
        'idType': idtype,
        'jnuid': jnuid
    }
    info_params = json.dumps(info_params)

    stuInfo = 'https://stuhealth.jnu.edu.cn/api/user/stuinfo'

    r = req.post(stuInfo,
                 data=info_params,
                 headers=play_load_header)

    message = json.loads(r.content)

    name = message['data']['xm'] # student's name

    # write health status and send it to main web

    dest = 'https://stuhealth.jnu.edu.cn/api/write/main'

    health_params = {
        "mainTable":{
            "wayStart":message['data']['mainTable']['wayStart'],
            "arriveTime":message['data']['mainTable']['arriveTime'],
            "way2Start":message['data']['mainTable']['way2Start'],
            "language":message['data']['mainTable']['language'],
            "declareTime":message['meta']['timestamp'].split(' ')[0],
            "personNo":message['data']['mainTable']['personNo'],
            "personName":message['data']['xm'],
            "sex":message['data']['xbm'],
            "professionName":message['data']['zy'],
            "collegeName":message['data']['yxsmc'],
            "phoneArea":message['data']['mainTable']['phoneArea'],
            "phone":message['data']['mainTable']['phone'],
            "assistantName":message['data']['mainTable']['assistantName'],
            "assistantNo":message['data']['mainTable']['assistantNo'],
            "className":message['data']['mainTable']['className'],
            "linkman":message['data']['mainTable']['linkman'],
            "linkmanPhoneArea":message['data']['mainTable']['linkmanPhoneArea'],
            "linkmanPhone":message['data']['mainTable']['linkmanPhone'],
            "personHealth":message['data']['mainTable']['personHealth'],
            "temperature":message['data']['mainTable']['temperature'],
            "personHealth2":message['data']['mainTable']['personHealth2'],
            "leaveState":message['data']['mainTable']['leaveState'],
            "leaveHubei":message['data']['mainTable']['leaveHubei'],
            "wayType1":message['data']['mainTable']['wayType1'],
            "wayType2":message['data']['mainTable']['wayType2'],
            "wayType3":message['data']['mainTable']['wayType3'],
            "wayType5":message['data']['mainTable']['wayType5'],
            "wayType6":message['data']['mainTable']['wayType6'],
            "wayTypeOther":message['data']['mainTable']['wayTypeOther'],
            "wayNo":message['data']['mainTable']['wayNo'],
            "currentArea":message['data']['mainTable']['currentArea'],
            "inChina":message['data']['mainTable']['inChina'],
            "personC1id":message['data']['mainTable']['personC1id'],
            "personC1":message['data']['mainTable']['personC1'],
            "personC2id":message['data']['mainTable']['personC2id'],
            "personC2":message['data']['mainTable']['personC2'],
            "personC3id":message['data']['mainTable']['personC3id'],
            "personC3":message['data']['mainTable']['personC3'],
            "personC4":message['data']['mainTable']['personC4'],
            "otherC4":message['data']['mainTable']['otherC4'],
            "isPass14C1":message['data']['mainTable']['isPass14C1'],
            "isPass14C2":message['data']['mainTable']['isPass14C2'],
            "isPass14C3":message['data']['mainTable']['isPass14C3']
        },
        "jnuid":jnuid
    }
    health_params = json.dumps(health_params)

    r = req.post(dest,
                 data=health_params,
                 headers=play_load_header)

    message = json.loads(r.content)

    # return feedback
    return message['meta']['timestamp'] + '\n' + name + ', ' + message['meta']['msg']

if __name__ == "__main__":
    msg = run()
    print(msg)