# 暨南大学打卡小助手

## 2021.5.7更新

支持daemon化，在`main.py`里的`attend_list`填上自己的学号密码，运行即可：

```bash
python3 main.py
```

daemon的pid在当前目录下的pidfile里，退出只需`kill`即可。

## 2021.2.3更新

直接给你们脚本，有用代码也就几十行，不多，大部分都是信息占行数。

使用前只需安装`Python3`和`Requests`库即可，之后按照代码里的注释操作(`Line 118`开始)。

自动打卡可能要配合服务器使用，没有服务器就还是手动，但是方便很多。

```bash
alias a="python3 /your-path-to/main.py" # 创建别名
a # 执行
```

每天记得打开命令行输入一下`a`就好了，就这样，使用愉快。