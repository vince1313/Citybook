from flask import Flask,render_template,jsonify,abort
from flask import request,url_for
from flask import make_response
from flask_sqlalchemy import SQLAlchemy
import json
import requests
from bs4 import BeautifulSoup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'THIS IS A SECRET KEY FOR API'
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:////Users/shendikai/Desktop/citybook-master/services.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#API数据库
class webservice(db.Model):
    id = db.Column(db.Interger,primary_key = True)
    task_id = db.Column(db.String, unique = True)
    task_songs = db.Column()
    def __init__(self,task_id,task_songs):
        self.task_id = task_id
        self.task_songs = task_songs
    def __repr__():
        return '<webservice%r>'%self.task_id
@app.before_first_request
def create_db():
    db.create_all
    db.session.add_all(tasks)
    db.session.commit()
#爬虫程序以调用API接口，获得歌曲ID
url = 'https://music.163.com/#/playlist'
r = requests.get(url).content
bsObj = BeautifulSoup(r,'lxml')
songs_id = bsObj.find('textarea').text
jsObj = json.loads(songs_id)
songIDS = []
for item in songs_id:
    songIDS.append(item['id'])
the_main_url = 'https://music.163.com/#/playlist?{}'.format(id = map(songIDS))
response = requests.get(the_main_url).content
json_url = json.loads(response)
s = request(json_url)
k = u"audio"
music_url = s['result']['songs'][0][k]
tasks = []
tasks.append(music_url)
#webservices入点
@app.route('/citysongs',method = ["GET"])
def post_songs():
    task = filter(lambda t :t['id'] == music_url,tasks)
    if len(task) == 0:
        abort(404)
    return jsonify(music_url)


#异常判断
@app.errorhandler(404)
def page_not_found():
    return make_response(jsonify({'error':'404'}),404)
#用户请求的数据
@app.route('/citysongs',method = ['POST'])
def create_tasks():
    if not request.json or not 'id' in request.json:
        abort(400)
    db.session.add(music_url)
    db.session.commit()
    return jsonify(music_url),201
#如果用户请求新的URI，调用此函数
def make_public_task(music_url):
    new_task = {}
    for field in tasks:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id = music_url['id'],external = True)
        else:
            new_task[field] = music_url[field]
    return new_task

#调用url重定向函数以完成用户重复请求
@app.route('/citysongs',mehthod = ['GET'])
def get_new_tasks():
    return jsonify({'tasks':map(make_public_task,tasks)})















if __name__ == "__main__":
    app.run(debug=True)




