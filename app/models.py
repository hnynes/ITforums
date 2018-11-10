from . import db


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
