import os
from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread


app = Flask(__name__)
app.config['SECRET_KEY'] = 'LGY DE MISHI' #使用密匙来对表格数据进行加密，防止受到跨站请求伪造，在一般情况下，密匙并不写入源码而是要保存在环境变量中
bootstrap = Bootstrap(app)


#配置mysql的相关信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://lgy:test-lgy-734190L@47.94.211.34:3306/forumit?charset=utf8'
#将SQLALCHEMY_TRACK_MODIFICATIONS设置为fasle以便在 不需要跟踪对象变化时降低内存消耗
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
#用户名和密码采取导入环境变量的形式防止密码泄露
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # '734190426@qq.com'
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') # 'irptfbwxnrvkbcig'
app.config['FLASKY_MAIL_SENDER'] = '734190426@qq.com'  # this is sender
app.config['FLASKY_ADMIN'] = '734190426@qq.com'  # this is the email of admin
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[FORUMIT]'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship('User', backref='role')
    #一个role实例的users属性返回与角色相关联用户的列表，backref属性向User模型中增加一个role属性，从而定义方向关系，user可以通过这个属性来获取获取相对的role模型
    #backref作用是在关系的另一个模型中增加反向引用
    def __repr__(self):#返回一个可读性的字符串便于调试
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True, index = True)#除此之外还需要为name创建索引
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) #增加一个外键用来将其与roles表连接起来

    def __repr__(self):
        return '<User %r>' % self.name



class Namefrom(FlaskForm):
    name = StringField(description='What is your name?', validators=[DataRequired()])
    submit = SubmitField('提交')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Namefrom()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            #db.session.commit()
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'], 'NEW USER', 'mail/newuser', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

#收件人地址、主题、渲染邮件正文的模板和关键字参数列表
def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject, sender = app.config['FLASKY_MAIL_SENDER'], recipients = [to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr



if __name__ == '__main__':
    app.run()
