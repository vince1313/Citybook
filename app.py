from flask import Flask,redirect,url_for,render_template,request
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,length
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY']="This is a secret key"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////Users/vincent.zhu/Desktop/城记/user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


#用户注册表单
class registerform(FlaskForm):
    nickname = StringField("昵称",validators=[InputRequired(message="昵称"),length(min=3,max=10,message="昵称在3～10位之间")])
    password = PasswordField('密码',validators=[InputRequired(message="密码"),length(min=6,max=20,message="密码在6～20位之间")])
    password_confirm = PasswordField(" 确认密码",validators=[InputRequired(message="确认密码"),length(min=6,max=20,message="")])
    email = StringField("邮箱 ",validators=[InputRequired(message=" 邮箱")])


#用户登陆表
class loginform(FlaskForm):
    email = StringField("邮箱 ",validators=[InputRequired(message=" 邮箱")])
    password = PasswordField('密码',validators=[InputRequired(message="密码")])


# 用户数据库
db = SQLAlchemy(app)
class citybookdb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    nickname = db.Column(db.String())
    password = db.Column(db.String())
    email = db.Column(db.String())

# 主页
@app.route('/')
def index():
    return render_template("index.html")

#城市单页
@app.route('/citybook')
def citybook():
    return render_template('citybook.html')


#注册页面
@app.route('/register',methods = ['GET','POST'])
def register():
    form = registerform()
    if form.validate_on_submit():
        if form.password.data == form.password_confirm.data:
            user = citybookdb(nickname=form.nickname.data, password =form.password.data, email = form.email.data)
            db.session.add(user)
            db.session.commit()
            return "注册成功"
    return render_template('register.html',form=form)


#登陆页面
@app.route('/login',methods =['GET','POST'])
def login():
    form = loginform()
    if form.validate_on_submit():
        matchdata = citybookdb.query.all()
        for u in matchdata:
            if form.email.data == u.email and form.password.data== u.password:
                return "登陆成功"
        return "您还没有注册 "
    return render_template('login.html',form = form)




if __name__ =="__main__":
    app.run(debug= True)
    