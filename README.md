# 暨南大学打卡小助手

### 提供了WIN和MAC版

win有GUI界面，而MAC没有，且要手动抓包



windows版，下载后看readme文档使用



Win下载地址：

链接：https://pan.baidu.com/s/18vaqfw8QjRmTGAm6ReD3mg 

提取码：cgwz

Mac直接clone mac文件夹到本地，手动抓包后，修改load.py的相应信息即可,再运行core.py
配合crontab可以自动打开
如：

sudo crontab -e
（ into vi edit...）
（enter:）
0 9 * * * python3 path-to-core.py
（ save adn quit）

即可
