from flask import Flask,redirect,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLAlCHEMY_DATABASE_URI']='sqlite:/Users/vincent.zhu/Desktop/citybook.db'


db = SQLAlchemy(app)
class citybookdb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(10))
    cityname =db.Column(db.String(10))
    citysong = db.Column(db.String(20))



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/citybook')
def citybook():
    return render_template('citybook.html')

@app.route('/register')
def register():
    return render_template('register.html')






if __name__ =="__main__":
    app.run(debug= True)
    
