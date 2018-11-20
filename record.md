# 记录搭建论坛系统之中学到的内容和遇见的问题以及解决方法

## day 1103
今天决定开始学习搭建论坛系统了，此后每天至少1个小时，周末的话八小时吧，不然真的赶不完工了，还有要准备实习好烦啊！

### 路由和视图函数：
客户端将请求发送给web服务器，web服务器再将请求转发给flask实例，flask实例需要知道对应每个URL要运行哪些代码，因此保存了一个URL到python代码的映射关系，处理URL和python函数关系的程序称之为路由。我们通常使用app.route装饰器来声明路由：
```python
@app.route('/')
def index():
    return '<h1>hello world!</h1>'
```
除此之外，还能够使用add_url_rule([URL],[端点名],[视图函数])方式来设置路由:
```python
def index('/'):
    return '<h2>test1!</h2>'

add_url_rule('/', 'index', index)
```
在日常使用浏览器时，我们通常会发现网站的url往往会随着你输入的一些东西而做出适配选择，比如你的github个人信息页面的URL为https://github.com/<your name>,python flask也支持这种形式的URL，只需要在app.route中使用特殊的语法即可如下：
```python
@app.route('/<name>')
def index(name):
    return '<h1>hello, {}</h1>'.format(name)
```
即放在url中尖括号内部的内容为动态可变化的内容，在调用视图函数的时候，flask会将动态的部分作为参数传入视图函数之中，路由中的动态部分默认使用字符串，但也支持使用int、float、path类型.使用int <code>'user/<int: id>'</code>.

### 运行第一个flask程序 hello，world
我们可以采取两种方式来运行flask程序
在命令行中输入命令启动  
```shell
(forum)$export FLASK_APP=hello.py
(forum)$flask run
* Serving Flask app "hello.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [03/Nov/2018 10:34:48] "GET / HTTP/1.1" 404 -
127.0.0.1 - - [03/Nov/2018 10:34:48] "GET /favicon.ico HTTP/1.1" 200 -
127.0.0.1 - - [03/Nov/2018 10:35:14] "GET /LGY HTTP/1.1" 200 -
127.0.0.1 - - [03/Nov/2018 10:35:14] "GET /favicon.ico HTTP/1.1" 200 -
```
在程序脚本之中加入启动命令，然后用python 运行启动脚本需要在hello.py 尾部加上：  
```python
if __name__ = '__main__':
    app.run()
```

### 同样的如果你想开启调试模式可以在命令行中输入 export FLASK_DEBUG=1
在这个模式下，开发服务器默认会加载两个便利的工具：重载器和调试器。
启用重载器后，Flask 会监视项目中的所有源码文件，发现变动时自动重启服务器。在开
发过程中运行启动重载器的服务器特别方便，因为每次修改并保存源码文件后，服务器都
会自动重启，让改动生效。
调试器是一个基于 Web 的工具，当应用抛出未处理的异常时，它会出现在浏览器中。此
时，Web 浏览器变成一个交互式栈跟踪，你可以在里面审查源码，在调用栈的任何位置计算表达式。

使用 app.run() 方法启动服务器时，不会用到 FLASK_APP 和 FLASK_DEBUG 环境
变量。若想以编程的方式启动调试模式，就使用 app.run(debug=True)。

需要注意的是：千万不要在生产服务器中启用调试模式。客户端通过调试器能请求执行远
程代码，因此可能导致生产服务器遭到攻击。作为一种简单的保护措施，
启动调试模式时可以要求输入 PIN 码，执行 flask run 命令时会打印在控制台中。

### 应用和请求上下文
flask程序在收到请求之后，可能会需要在视图函数中使用这些请求内容，为了让视图函数使用请求对象，一方面我们可以在视图函数中传入请求对象，不过这会让视图函数参数变多，除了请求对象，如果视图函数还需要处理其他对象，这时视图函数就会变得比较复杂，为了避免这种情况，flask引入了请求上下文，临时地把这些对象变成全局可以访问形式。
(需要特别注意的是这些上下文并不是全局变量，往往存在着适用区域，需要特别的注意其使用，否则就会报错，我之前遇到过几次之前还很疑惑为什么，在读一遍感觉好像找到了问题所在，一会去实验一下)
flask中有两种形式的上下文，分别是应用上下文和请求上下文：   

变量名       上下文               说　明
current_app 应用上下文      当前应用的应用实例
g           应用上下文      处理请求时用作临时存储的对象，每次请求都会重设这个变量
request     请求上下文      请求对象，封装了客户端发出的 HTTP 请求中的内容
session     请求上下文      用户会话，值为一个字典，存储请求之间需要“记住”的值

flask在分派请求之前激活或推送应用和请求上下文，请求处理完成之后再将其删除，应用上下文被推送之后，就可以在__当前线程__使用g和current_app变量，请求上下文与之类似。

### 请求的分派机制
应用在收到客户的请求之后，会找到对应的处理该请求的视图函数，flask是通过应用的URL映射关系来查找请求的URL，我们可以通过在python shell中产看对应的映射关系。
```python shell
from hello import app
app.url_map
```
URL 映射中的 (HEAD, OPTIONS, GET) 是请求方法，由路由进行处理。HTTP 规范中规定，
每个请求都有对应的处理方法，这通常表示客户端想让服务器执行什么样的操作。Flask
为每个路由都指定了请求方法，这样即使不同的请求方法发送到相同的 URL 上时，也会
使用不同的视图函数处理。HEAD 和 OPTIONS 方法由 Flask 自动处理，因此可以这么说，在
这个应用中，URL 映射中的 3 个路由都使用 GET 方法（表示客户端想请求信息，例如一个
网页）  

### 请求钩子
在使用场景之中我们经常会遇到需要在请求之后或者请求之前执行代码的情况，比如在请求开始的时候，我们可能会需要在请求开始时，我们可能需要创
建数据库连接或者验证发起请求的用户身份。__为了避免在每个视图函数中都重复编写代码,Flask 提供了注册通用函数的功能__，注册的函数可在请求被分派到视图函数之前或之
后调用。
请求钩子通过装饰器实现。Flask 支持以下 4 种钩子。
before_request
注册一个函数，在每次请求之前运行。
before_first_request
注册一个函数，只在处理第一个请求之前运行。可以通过这个钩子添加服务器初始化任务。
after_request
注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
teardown_request
注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。
**在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g。例如，before_request 处理程序可以从数据库中加载已登录用户，并将其保存到 g.user 中。随后调用视
图函数时，便可以通过 g.user 获取用户。**

### 请求的响应


### 模板
视图函数的作用很明确就是生成请求的响应，但是这种模式并不适用大多数情况，很多情况下，请求会改变应用的状态，这种变化往往会在视图函数中实现。
以用户在网站中注册新账户的过程为例。用户在表单中输入电子邮件地址和密码，然后点
击提交按钮。服务器接收到包含用户输入数据的请求，然后 Flask 把请求分派给处理注册
请求的视图函数。这个视图函数需要访问数据库，添加新用户，然后生成响应回送浏览
器，指明操作成功还是失败。这两个过程分别称为业务逻辑和表现逻辑。
**把业务逻辑和表现逻辑混在一起会导致代码难以理解和维护**。假设要为一个大型表格构建
HTML代码，表格中的数据由数据库中读取的数据以及必要的 HTML 字符串连接在一起。
把表现逻辑移到模板中能提升应用的可维护性。

### jinja2模板的使用

### jinja2中的变量
在模板中我们用{{  }}结构来表示一个占位符，用来告诉模板引擎，这个位置的值从渲染模板时使用的数据中获得。
jinja2能够识别几乎所有类型的变量，比如字典、列表和对象
```HTML
<p>A value from a dictionary: {{ mydict['key'] }}.</p>
<p>A value from a list: {{ mylist[3] }}.</p>
<p>A value from a list, with a variable index: {{ mylist[myintvar] }}.</p>
<p>A value from an object's method: {{ myobj.somemethod() }}.</p>
```
除此之外，变量的值还能使用过滤器来修改过滤器添加在变量名之后，中间用|隔开，比如hello, {{ name|capitalize }}!,就是将name转换成大写形式。
常用的过滤器如下：  
过滤器名      说　明
safe        渲染值时不转义
capitalize  把值的首字母转换成大写，其他字母转换成小写
lower       把值转换成小写形式
upper       把值转换成大写形式
title       把值中每个单词的首字母都转换成大写
trim        把值的首尾空格删掉
striptags   渲染之前把值中所有的 HTML 标签都删掉

### jinja2的控制结构
具体使用见电子书

### 模板继承机制

### 链接
具有多个路由的应用一般都需要可以链接不同页面的链接，比如导航栏.在模板中直接编写简单路由的URL链接并不难，但是对于动态路由，在模板中构建正确的URL链接就比较困难了，除此之外，直接编写URL还可能会对代码中的路由产生依赖关系，一旦路由发生改变，模板中对应的URL链接也需要改变，否则链接就会失效。为了解决上述问题，flask中提供了url_for()函数，他使用保存的URL映射信息生成URL。
url_for()的用法就是以视图函数名作为参数，url_for('index') 得到的结果是 /，即应用的根 URL。调用 url_for('index', _external=True)
返回的则是绝对地址，在这个示例中是 http://localhost:5000/。
__生成连接应用内不同路由的链接时，使用相对地址就足够了。如果要生成在浏览器之外使用的链接，则必须使用绝对地址，例如在电子邮件中发送的链接。__
使用 url_for() 生成动态 URL 时，将动态部分作为关键字参数传入。例如，url_for('user',name='john', _external=True) 的返回结果是 http://localhost:5000/user/john。
传给 url_for() 的关键字参数不仅限于动态路由中的参数，非动态的参数也会添加到查询字符串中。例如，url_for('user', name='john', page=2, version=1) 的返回结果是 /user/john?page=2&version=1。

### 静态文件
默认设置下，Flask 在应用根目录中名为 static 的子目录中寻找静态文件。如果需要，可在static 文件夹中使用子文件夹存放文件。服务器收到映射到 static 路由上的 URL 后，生成
的响应包含文件系统中对应文件里的内容。


### 表单

表4-1：WTForms支持的HTML标准字段
字段类型             说　明
BooleanField        复选框，值为 True 和 False
DateField           文本字段，值为 datetime.date 格式
DateTimeField       文本字段，值为 datetime.datetime 格式
DecimalField        文本字段，值为 decimal.Decimal
FileField           文件上传字段
HiddenField         隐藏的文本字段
MultipleFileField   多文件上传字段
FieldList           一组指定类型的字段
FloatField          文本字段，值为浮点数
FormField           把一个表单作为字段嵌入另一个表单
IntegerField        文本字段，值为整数
PasswordField       密码文本字段
RadioField          一组单选按钮
SelectField         下拉列表
SelectMultipleField 下拉列表，可选择多个值
SubmitField         表单提交按钮
StringField         文本字段
TextAreaField       多行文本字段
WTForms             内建的验证函数如表 4-2 所示。

表4-2：WTForms验证函数
验证函数                 说　明
DataRequired           确保转换类型后字段中有数据
Email                  验证电子邮件地址
EqualTo                比较两个字段的值；常用于要求输入两次密码进行确认的情况
InputRequired          确保转换类型前字段中有数据
IPAddress              验证 IPv4 网络地址
Length                 验证输入字符串的长度
MacAddress             验证 MAC 地址
NumberRange            验证输入的值在数字范围之内
Optional               允许字段中没有输入，将跳过其他验证函数
Regexp                 使用正则表达式验证输入值
URL                    验证 URL
UUID                   验证 UUID
AnyOf                  确保输入值在一组可能的值中
NoneOf                 确保输入值不在一组可能的值中
### 视图函数中处理表单
app.route 装饰器中多出的 methods 参数告诉 Flask，在 URL 映射中把这个视图函数注册为
GET 和 POST 请求的处理程序。如果没指定 methods 参数，__则只把视图函数注册为 GET 请求的
处理程序。__
这里有必要把 POST 加入方法列表，因为更常使用 POST 请求处理表单提交。表单也可以通过
GET 请求提交，但是 GET 请求没有主体，提交的数据以查询字符串的形式附加到 URL 中，在
浏览器的地址栏中可见。基于这个以及其他多个原因，处理表单提交几乎都使用 POST 请求。
局部变量 name 用于存放表单中输入的有效名字，如果没有输入，其值为 None。如上述代
码所示，我们在视图函数中创建了一个 NameForm 实例，用于表示表单。提交表单后，如果
数据能被所有验证函数接受，那么 validate_on_submit() 方法的返回值为 True，否则返回
False。这个函数的返回值决定是重新渲染表单还是处理表单提交的数据。
用户首次访问应用时，服务器会收到一个没有表单数据的 GET 请求，所以 validate_on_
submit() 将返回 False。此时，if 语句的内容将被跳过，对请求的处理只是渲染模板，并
传入表单对象和值为 None 的 name 变量作为参数。用户会看到浏览器中显示了一个表单。
用户提交表单后，服务器会收到一个包含数据的 POST 请求。validate_on_submit() 会调用名
字字段上依附的 DataRequired() 验证函数。如果名字不为空，就能通过验证，validate_on_
submit() 返回 True。现在，用户输入的名字可通过字段的 data 属性获取。在 if 语句中，把
名字赋值给局部变量 name，然后再把 data 属性设为空字符串，清空表单字段。因此，再次
渲染这个表单时，各字段中将没有内容。最后一行调用 render_template() 函数渲染模板，
但这一次参数 name 的值为表单中输入的名字，因此会显示一个针对该用户的欢迎消息。

即在提交表单时常常使用post请求，当然也能使用get请求，但是get请求没有主体，提交的数据以查询字符串的形式附加到URL中，在浏览器的地址栏可见。

### 重定向和用户会话
上述实现的代码存在一个可用性问题，用户在提交表单之后，一旦点击了刷新按钮，此时会看到一个警告，要求确认是否要重新提交表单，之所以出现这种情况，是因为在刷新之后，浏览器会重新发送原来发送过的请求，如果前一个请求是包含表单的post请求，再刷新之后会再次提交表单，在大多数情况下，这并不是我们想要的结果，所以浏览器会对用户做出提醒，很多用户不理解这个警告，因此我们在设计时最好不要把Post请求作为浏览器发出的最后一个请求。
为了解决上述问题，我们采用将重定向作为post请求的响应，重定向作为一种特殊的响应，__其不同之处在于其返回的是URL而不是html代码__，浏览器在收到重定向之时，会向重定向的URL发出get请求，以显示页面的内容，此过程可能需要多花几毫秒的时间,而此时前一个请求是get请求，用户就可以随意的点击刷新按钮，并且不会得到警告，这种技巧叫做**post/重定向/get**
但是不要想当然，使用这种方式会出现另一种后果，就是应用在处理post请求时，从中获取相关的数据，但是一旦post请求完后，数据也就随之不见了。因此该应用应该能够保存相关的数据这样在重定向之后，仍然能够使用相关的数据，从而构成真正的响应。为了解决这种问题，采用用户会话的形式，应用可以把数据存储在用户会话中，以便在请求之间“记住”数据。用户会话是一种私有存储，每个连接到服务器的客户端都可访问。我们在前面介绍过用户会话，它是请求上下文中的变量，名为 session，像标准的 Python 字典一样操作。
### 数据库部分
论坛系统最重要的部分在我看来就是数据库的设计部分，在存储用户信息的话我打算利用利用mysql来存储，其他的先不说可能会用上redis，在中期报告之前先完成基本的HTML页面，以及注册功能的实现，要求能够发送邮件来进行获取验证码等功能。
#### 数据库设计
mysql关系型数据库，我打算建两个表分别是用户和角色，这样比较好能更加便捷管理关系。角色分为普通用户和管理员。
具体的设计细节后续补上

#### 安装flask-sqlalchemy
为了使用sql相关语句比较方便

几种流行数据库引擎使用的url格式如下：
MySQL                  mysql://username:password@hostname/database
Postgres               postgresql://username:password@hostname/database
SQLite（Linux，macOS） sqlite:////absolute/path/to/database
SQLite（Windows）      sqlite:///c:/absolute/path/to/database
我们在配置数据库的相关内容时往往采取将配置信息存储在config.py文件中
在这些 URL 中，hostname表示数据库服务所在的主机，可以是本地主机（localhost），也可以是远程服务器。数据库服务器上可以托管多个数据库，因此 database 表示要使用的数据库名。如果数据库需要验证身份，使用 username 和 password 提供数据库用户的凭据。

比如我使用的是mysql其配置信息为：
mysql://lgy:test-lgy-734190L@47.94.211.34:3306/forumit?charset=utf8


一对一关系可以用前面介绍的一对多关系表 示，但调用 db.relationship() 时要把 uselist 设为 False，把“多”变成“一”。多对一 关系也可使用一对多表示，对调两个表即可，或者把外键和db.relationship() 都放在 “多”这一侧。最复杂的关系类型是多对多，需要用到第三张表，这个表称为关联表（或 联结表）

数据库的相关操作
>>> from hello import db
>>> db.create_all()
>>> from hello import Role,User
>>> admin=Role(name='Admin')
>>> comuser=Role(name='user')
>>> user1=User(name='lgy',role=admin)
>>> user2=User(name='test1',role=comuser)

如果你退出了 shell 会话，前面这些例子中创建的对象就不会以 Python 对象的形式存在， 但在数据库表中仍有对应的行。如果打开一个新的 shell 会话，要从数据库中读取行，重新 创建 Python 对象。下面这个例子发起一个查询，加载名为 "User" 的用户角色：
>>> user_role = Role.query.filter_by(name='User').first()

### 集成python-shell
每次启动 shell 会话都要导入数据库实例和模型，这真是份枯燥的工作。为了避免一直重复 导入，我们可以做些配置，让 flask shell 命令自动导入这些对象。
若想把对象添加到导入列表中，必须使用 app.shell_context_processor 装饰器创建并注册 一个 shell 上下文处理器.
添加一个 shell 上下文处理器
@app.shell_context_processor
def make_context():
    return dict(db=db, User=User, Role=Role)
这个 shell 上下文处理器函数返回一个字典，包含数据库实例和模型。除了默认导入的 app 之外，flask shell 命令将自动把这些对象导入 shell。

### 数据库迁移
使用flask-migrate对数据库进行迁移，在进行应用的开发的时候经常会发现需要修改数据库的结构，更新表的方式往往是先删除旧表在创建新表，但是需要注意的是数据库中往往已经存储了一些数据，而一旦删除之前的旧表，数据库中的这些数据也会随之删除，在开发过程中，更加常用的是数据库迁移技术，这种技术能够追踪数据库的版本更新记录，并以增量的方式将改变应用到数据库之中。SQLAlchemy的开发人员名为 Alembic。除了直接使用 Alembic 之 外，Flask 应用还可使用 Flask-Migrate 扩展。这个扩展是对 Alembic 的轻量级包装，并与 flask 命令做了集成。


使用指南 在发送邮件之时，需要先导入环境变量
export FLASK_APP=hello.py
export MAIL_USERNAME=734190426@qq.com
export MAIL_PASSWORD=irptfbwxnrvkbcig
export FLASKY_ADMIN=<the mail address you want to send> 在实现注册功能时，这个地方的数据由用户填写的表格中获取


### 发送邮件
为了避免在发送邮件的时候出现停滞，在这里采取多线程处理，单独为发送邮件程序分配一个线程，让其去独立执行，而浏览器的页面则不会因此而阻塞。
在使用多线程的时候我们需要注意的是，flask许多的扩展都是默认假设存在激活的应用上下文和请求上下文，需要注意的Flask_mail中的send()函数需要应用上下文current_app,因此必须激活应用上下文，而在线程之中，上下文与线程是配套的，在不同的线程中执行mail.send()需要用app.app_context()人工来创造上下文，将app作为传入参数传入线程之中。


### 重新规划项目的结构使其便于管理
应用包用于存放应用的所有代码、模板和静态文件。我们可以把这个包直接称为 app（应 用），如果有需求，也可使用一个应用专属的名称。templates 和 static 目录现在是应用包
的一部分，因此要把二者移到 app 包中。数据库模型和电子邮件支持函数也要移到这个包 中，分别保存为 app/models.py 和 app/email.py。

**使用配置文件来导入配置选项**
大多数应用不止需要一份配置。生产服务器和开发期间使用的服务器应该各有一份单独的配置。处理这个的最简单方法是，使用一份默认的总会被载入的配置，和一部分版本控制，以及独立的配置来像上面提到的例子中必要的那样覆盖值:

#### 使用应用工厂函数
在单个文件中开发应用我们在一开始可能回觉这种方式简单明了，但是随着应用具备的功能越来越多，代码量越来越大，这时去修改代码就变得比较困难了，因为你为觉得无从下手，改了一个变量还要担心其连锁反应，在实际的项目开发之中为了解决这个问题，采取了延迟创建应用实例的方法，将创建的过程迁移到可显示调用的工厂函数之中，这种方法不仅能够可以给脚本留出配置应用的时间，还能够创建多个应用实例，为测试提供方便。

在应用工厂函数中我们导入配置文件 使用from_object()方法其具体的使用细节可以查看文档链接如下[Flask config文件怎样导入](http://docs.jinkan.org/docs/flask/config.html)

构造文件(__init__.py)导入了大多数正在使用的 Flask 扩展。由于尚未初始化所需的应用实例，所以创建扩展类时没有向构造函数传入参数，因此扩展并未真正初始化。create_app() 函数是应用的工厂函数，**接受一个参数，是应用使用的配置名。配置类在 config.py 文件中定义，其中保存的配置可以使用 Flask app.config 配置对象提供的 from_object() 方法直接导入应用。至于配置对象，则可以通过名称从 config 字典中选择。应用创建并配置好后，就能初始化扩展了。在之前创建的扩展对象上调用 init_app() 便可以完成初始化。**
现在，应用在这个工厂函数中初始化，使用 Flask 配置对象的 from_object() 方法，其参数 为 config.py 中定义的某个配置类。此外，这里还调用了所选配置的 init_app() 方法，以便执行更复杂的初始化过程。
工厂函数返回创建的应用示例，不过要注意，现在工厂函数创建的应用还不完整，因为没有路由和自定义的错误页面处理程序
#### 在蓝本中实现应用功能
由于引入了工厂函数这样定义路由的操作就变得复杂了很多，在单脚本应用中，应用实例存在于全局的作用域之中，路由可以直接用app.route来定义，但是现在应用在运行时创建，只有在调用了create_app()方法后才能够定义路由，但是这时定义路由就晚了。自定义的错误页面处理程序也面临着这样的问题，因为错误页面处理程序需要用app.errorhandler装饰器来修饰。
有了问题，一定会有相应的处理措施，这已经是老套路了，在flask中，它使用蓝本(blueprint)来解决这个问题，蓝本和应用相似，其也能定义路由和错误处理程序，但是不同之处在于，蓝本定义的路由和错误处理程序处于休眠状态，直到蓝本注册到应用上之后，他们才真正的成为应用的一部分。使用处于全局作用的蓝本时，其路由和错误处理程序的定义方法几乎和单脚本中定义的方法相同。

蓝本通过实例化一个Blueprint 类对象创建。这个构造函数有两个必须指定的参数：蓝本的名称和蓝本所在的包或模块。与应用一样，多数情况下第二个参数使用 Python 的 __ name__ 变量即可.

应用的路由保存在主蓝本同一个目录下的views.py中，错误处理程序则保存在同一个目录下的errors.py之中，在主蓝本中导入这两个模板能够将蓝本与路由联系起来。。注意，这 些模块在 app/main/__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，因为在 app/ main/views.py 和 app/main/errors.py 中还要导入 main 蓝本，所以除非循环引用出现在定义 main 之后，否则会致使导入出错。


### 用户身份验证

#### 使用werkzeug来对用户输入的密码进行加密








#### 使用Flask_login
LoginManager中的login_view属性文档之中是这样定义的
login_view (str) – The name of the login view. (Alternately, the actual URL to the login view.)
即指向登录路由，因此在工厂函数中这样声明：login_manager.login_view = 'authority.login' 即使用蓝本.登录路由的形式

flask_login的工作原理：
在使用flask_login时，需要我们提供一个user_loader()回调，用来从根据用户ID从会话中存储的用户中重新加载用户对象。它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。

如果 ID 无效的话，它应该返回 None (而不是抛出异常)。(在这种情况下，ID 会被手动从会话中移除且处理会继续)
在文档中user_loader的定义如下：
user_loader(callback)[source]
This sets the callback for reloading a user from the session. The function you set should take a user ID (a unicode) and return a user object, or None if the user does not exist.

Parameters:	callback (callable) – The callback for retrieving a user object.
这个回调在models.py中设置

login_manager.user_loader 装饰器把这个函数注册给 Flask-Login，在这个扩展需要获取已 登录用户的信息时调用。传入的用户标识符是个字符串，因此这个函数先把标识符转换成 整数，然后传给 Flask-SQLAlchemy 查询，加载用户。正常情况下，这个函数的返回值必 须是用户对象；如果用户标识符无效，或者出现了其他错误，则返回 None


在使用用户类之时要求实现下列的属性与方法
- is_authenticated
当用户通过验证时，也即提供有效证明时返回 True 。（只有通过验证的用户会满足 login_required 的条件。）
- is_active
如果这是一个活动用户且通过验证，账户也已激活，未被停用，也不符合任何你 的应用拒绝一个账号的条件，返回 True 。不活动的账号可能不会登入（当然， 是在没被强制的情况下）。
- is_anonymous
如果是一个匿名用户，返回 True 。（真实用户应返回 False 。）
- get_id()
返回一个能唯一识别用户的，并能用于从 user_loader 回调中加载用户的 unicode 。注意着 必须 是一个 unicode —— 如果 ID 原本是 一个 int 或其它类型，你需要把它转换为 unicode 。
除此之外要简便地实现用户类，你可以从 UserMixin 继承，它提供了对所有这些方法的默认实现，基本上能够满足需求。（虽然这不是必须的。）

匿名用户
默认情况下，当一个用户没有真正地登录，current_user 被设置成一个 AnonymousUserMixin 对象。它由如下的属性和方法:

is_active 和 is_authenticated 的值为 False
is_anonymous 的值为 True
get_id() 返回 None
如果需要为匿名用户定制一些需求(比如，需要一个权限域)，你可以向 LoginManager 提供一个创建匿名用户的回调（类或工厂函数）:

login_manager.anonymous_user = MyAnonymousUser


### 保护路由
使用login_required装饰器，如果未经过身份验证的用户访问这个路由，flask_login将拦截这个请求，并且重定向到登录页面，**我们可以在需要用户登录的的视图用 login_required 装饰器来装饰。**

### login_user的使用
如果密码正确，调用 Flask-Login 的 login_user() 函数，在用户会话中 把用户标记为已登录。login_user() 函数的参数是要登录的用户，以及可选的“记住我” 布尔值，“记住我”也在表单中勾选。如果这个字段的值为 False，关闭浏览器后用户会话 就过期了，所以下次用户访问时要重新登录。如果值为 True，那么会在用户浏览器中写入 一个长期有效的 cookie，使用这个 cookie 可以复现用户会话。cookie 默认记住一年，可以 使用可选的 REMEMBER_COOKIE_DURATION 配置选项更改这个值。

### 登录时使用的重定向机制 next
用户在访问未授权的页面时会跳转到登录页面，Flask_login中利用next来存储原URL，next是一个字符串参数，这个参数可以从request.args字典中读取，若查询字符串中没有next参数，则会重定向到首页。next参数中的url会经过验证，确保是相对URL，防止恶意用户利用这个参数把不知情的用户重定向到其他网站。

### 登录时的CERF保护


### 数据库迁移
(1) 对模型类做必要的修改。
(2) 执行 flask db migrate 命令，自动创建一个迁移脚本。
(3) 检查自动生成的脚本，根据对模型的实际改动进行调整。
(4) 把迁移脚本纳入版本控制。
(5) 执行 flask db upgrade 命令，把迁移应用到数据库中。


### 注册账户时的验证
我们在注册账户时需要验证用户提供的信息是否正确，比如用户提供的邮箱，为了达到这个目的我们需要在注册时，向用户提供的邮箱发送一个邮件，这时待注册的账户被我们标记为待确认状态，只有用户点击邮件中指定的连接，账号注册才算完成，账号才能使用，下面就记录一下如何实现这个功能。

为了实现这个功能，我们首先要思考怎样生成一个特定的确认链接，太简单的链接肯定不行，容易被解密，用户能恶意的去确认所有用户，可能会导致邮箱真正的所有者无法使用自己的邮箱去注册。除此之外该链接还应该有一定的时效机制，一但超出一定的时间，该链接就会失效，注册的用户也就会被撤销。
itsdangerous 提供了多种生成令牌的方法。其中，TimedJSONWebSignatureSerializer 类生 成具有过期时间的JSON Web 签名（JWS）。这个类的构造函数接收的参数是一个密钥， 在 Flask 应用中可使用 SECRET_KEY 设置。dumps() 方法为指定的数据生成一个加密签名，然后再对数据和签名进行序列化，生成令 牌字符串。expires_in 参数设置令牌的过期时间，单位为秒。为了解码令牌，序列化对象提供了 loads() 方法，其唯一的参数是令牌字符串。这个方法 会检验签名和过期时间，如果都有效，则返回原始数据。如果提供给 loads() 方法的令牌 无效或是过期了，则抛出异常。


在这里我打算利用



### 邮件内部生成URL的问题
默认情况下，url_for() 生成相对URL，例如url_for('auth.confirm', token='abc') 返 回的字符串是 '/auth/confirm/abc'。这显然不是能够在电子邮件中发送的正确 URL，因 为只有 URL 的路径部分。相对 URL 在网页的上下文中可以正常使用，因为浏览器会添加 当前页面的主机名和端口号，将其转换成绝对 URL。但是通过电子邮件发送的 URL 并没 有这种上下文。添加到 url_for() 函数中的 _external=True 参数要求应用生成完全限定的 URL，包括协议（http:// 或 https://）、主机名和端口。



### 项目结构重构
为了后续开发更加方便，现决定对项目进行重构
项目app下主要分为三个模块
frontstage模块 即普通用户使用的模块
cms模块  后台管理人员使用的模块
common模块 公有的模块

每个模块下都具有其自己对应的蓝图 以及数据库模型、表单类型等文件，这样建立项目结构是为了防止功能复杂之时维护不便之处
2018/11/14 当前为了不影响之前实现的功能，我并不敢直接删除源代码  需要逐渐的进行代码迁移  ，本周的主要工作即为实现项目重构，事项登录注册功能，并增加登录时的验证码功能，除此之外还要进行前端代码的丰富，使论坛的雏形基本具备，从而提交中期报告。


2018/11/15
我在程序包中的utils/tools.py里创建了generate_token（）函数和validate_token（）函数，分别用于创建和验证令牌。具体代码见tools.py文件 取代了之前在models.py文件中的创建令牌检验令牌函数

2018/11/16
开始后台登录的页面前端设计
采取利用bootstrap的模板来简化我们的前端设计工作打开bootstarp官网，查看使用样例，复制其登录样例的源代码到templates下的cms/cms_login.html文件之中
当然其html需要我们进行一些修改工作  举个例子，我们需要将其使用js和css文件下载到本地，并使用flask的静态路径引用方式来修改。


cms后台的路由设计
