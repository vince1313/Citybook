from flask import Flask,redirect,url_for,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField,PasswordField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired,length,DataRequired
from flask_wtf import FlaskForm



app = Flask(__name__)
app.config['SECRET_KEY']="This is a secret key"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////Users/shendikai/Desktop/citybook-master/user.db"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////Users/shendikai/Desktop/citybook-master/articles.db"
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////Users/shendikai/Desktop/citybook-master/images.db"
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







#下面是我的部分




#图片数据库
class imagedb(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer,primary_key=True)
    imageFiles = db.Column()
    db.create_all()
    def __repr__(self):
        return '<imagedb %r>'%self.name

#文章数据库
class articlesdb(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key = True)
    article = db.Column(db.String(800), unique = True)
    db.create_all()
    def __repr__(self):
        return '<articlesdb %r>'%self.name


#文章提交表
class editForm(FlaskForm):
    user = StringField(u'城记1',validators=[DataRequired(message=u'城记不可为空')])
    submitButton = SubmitField(u'提交文章')

#图片提交表
class AttachForm(FlaskForm):
    attach = FileField('请上传',validators = [FileAllowed(attach,'请上传为图片格式的文件')])


#异常抛出
@app.errorhandler(404)
def page_not_found(e):
    render_template('404.html'),404
    
@app.errorhandler(500)
def internal_server_error(e):
    render_template('500.html'),500


#文章界面
@app.route('/xiewenzhang',methods=['GET','POST'])
def xiewenzhang():
    form = editForm()
    article = None
    pictureForm = AttachForm()
    thePic = None
    if request.POST and form.validate_on_submit() and pictureForm.validate_on_submit():
        article = articlesdb(form.article.data)  
        db.session.add(article)
        db.session.commit()
        form.article.data = ''
        thePic = imagedb(pictureForm.photo.data)
        db.session.add(pictureForm)
        db.session.commit()
        pictureForm.thePic.data = None
        return redirect(url_for('xiewenzhang'))
    return render_template(xiewenzhang.html,form =form ,pictureForm=pictureForm)





   











    
    




if __name__ =="__main__":
    app.run(debug= True)
    