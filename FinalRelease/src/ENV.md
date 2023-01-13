### 环境配置文档

#### 项目虚拟环境配置

https://code.visualstudio.com/docs/python/environments#_work-with-environments

macOS/Linux

`python3 -m venv .venv`

windows:

`python -m venv .venv`

#### Windows PowerShell权限问题

默认情况下powershell执行脚本是受限的
在powershell中输入命令查看状态

`Get-ExecutionPolicy -list`

输入以下命令fix问题

`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

#### VSCode激活虚拟环境

命令面板Python: Select Interpreter -> ./venv.... (虚拟环境成功安装的话recommend的就是这个

powershell会自动运行.venv/Scripts/Activate.ps1

看到 `(.venv) PS D:\\cs3604>`就成功了

#### 安装依赖/导出依赖

powershell进入(.venv)后

`pip install -r requirements.txt`

如果添加了新的第三方依赖库，需要导出requirements.txt并提交到git仓库

`pip freeze -l > requirements.txt`

#### VSCode Flask debug模式

in `.vscode/launch.json`

复制，粘贴

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_DEBUG": "True",
            },
            "args": [
                "run"
            ],
            "jinja": true
        }
    ]
}
```

然后按F5直接就可以进行debug

#### PYTHONPATH配置项目跟路径(非必要)

https://code.visualstudio.com/docs/python/environments#_use-of-the-pythonpath-variable

in `.vscode/settings`:

"python.envFile": "${workspaceFolder}/.env",
"terminal.integrated.env.windows": {
  "PYTHONPATH": "src"
}
这里把初始配置放在.vscode.default/ 覆盖到.vscode/即可

in .env

PYTHONPATH=src