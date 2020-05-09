from selenium import webdriver
from browsermobproxy import Server # observe network
import json # load and save file
import sys # judge platform

def init():
    school_id = None
    password = None
    # origin file includes [id,pw]
    with open(r".\data\origin.json",'r') as f:
        school_id, password = json.load(f)


    server = Server(r'.\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')

    server.start()
    proxy = server.create_proxy()

    chrome_options = webdriver.ChromeOptions()
    # setting options
    chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
    # configuring proxy addr
    chrome_options.add_argument("--ignore-certificate-errors")
    # ignore ssl

    proxy.new_har("stuhealth",
                    options={
                        'captureHeaders':True,
                        'captureContent':True
                    }
                )
    # configuring infos should be marked down in har file

    driver = webdriver.Chrome(executable_path=r'.\driver\chromedriver.exe',
                            options=chrome_options
                            )
    driver.get("https://stuhealth.jnu.edu.cn")

    driver.find_element_by_id('zh').clear()
    driver.find_element_by_id('zh').send_keys(school_id)

    driver.find_element_by_id('passw').clear()
    driver.find_element_by_id('passw').send_keys(password)

    driver.find_element_by_xpath('/html/body/app-root/app-login/\
    div[2]/div[2]/form/div[4]/div/button').click()

    # save passwd file
    postData = proxy.har['log']['entries'][12]['request']['postData']['text']
    print(postData)
    postData = eval(postData)
    with open(r".\data\password.json","w") as f:
        json.dump(postData,f)


    # stop
    server.stop()
    driver.quit()
    proxy.close()
    # init successfully
    return True