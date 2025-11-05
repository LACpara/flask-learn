### 管理环境变量

#### 1. 程序发现机制

运行 `flask run` 时。若主程序名不为 `app.py` 或 `wsgi.py` 而是其他名称，则会产生错误提示：

`Error: Could not locate a Flask application`

如果希望使用其他名称，则需要修改环境变量 `FLASK_APP` 为相应的名称。可采用如下命令进行设置：

```bash
$ export FLASK_APP=hello.py
```

```cmd
set FLASK_APP=hello.py
```

```power
$env:FLASK_APP = "hellp.py"
```

也可以通过运行时的命令选项 `--app` 来进行设置：

```shell
flask --app hello.py run --debug
## --debug 启用调试模式，当程序出错时会显示错误信息；代码出现变动后程序会自动重载
```

或者可以使用库 `dotenv` 进行环境变量的管理：

```bash
$ pip install python-dotenv
$ touch .env .flaskenv
```

其中 `flaskenv` 用来存储 Flask 命令行系统相关的公开环境变量；而 `.env` 则用来存储敏感数据（因此要把它纳入 `.gitignore` 文件中）。