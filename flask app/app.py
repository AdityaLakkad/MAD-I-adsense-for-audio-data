import bcrypt
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request, session, redirect
from flask import jsonify
from bson.json_util import dumps
from bson.json_util import loads

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/MAD_I_BDAD'

mongo = PyMongo(app)

@app.route('/index')
def index():
    link = ["www.adityalakkad.ml","www.adityalakkad.ml","www.adityalakkad.ml"]
    l = ["cake.png","cake.png","cake.png"]
    return render_template('index.html', img = l, link=link)

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def loginget():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username' : request.form['username'], 'password' : request.form['password']})
        ads = mongo.db.advertisements.find({})
        tags = login_user['tags']
        print(login_user)
        if login_user:
            x = True
            l = []
            link = []
            if len(tags) < 3:
                link = ["www.divinesystems.in","www.adityalakkad.ml","www.adityalakkad.ml"]
                l = ["cake.png","cake.png","cake.png"]
                return render_template('index.html',img=list(l),link=list(link),lu=login_user['_id'])
            while x:
                for i in ads:
                    for j in tags:
                        if j in i['tags']:
                            if i['image'] not in l:
                                l.append(i['image'])
                                link.append(i['redirect'])
                        if len(l) >= 3:
                            x = False
                            break
            return render_template('index.html',img=list(l),link=list(link),lu=login_user['_id'],cake="cake.png")

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

########################################################
#                         APIs                         #
########################################################
@app.route('/api/v1/getString', methods=['GET'])
def getString():
    data = mongo.db.OLTP_SpeechData.find();
    print(data)
    print(loads(dumps(data)))
    return jsonify(loads(dumps(data)))

@app.route('/api/v1/pushString', methods=['POST'])
def pushString():
    print(request.json)
    table = mongo.db.OLTP_SpeechData
    s = table.find_one({'user_id':request.json['user_id']})
    if s:
        temp = s['string'] 
        table.update({'user_id':request.json['user_id']},{'$set':{'string':temp + request.json['string']}})
    else:
        userid = request.json['user_id']
        string = request.json['string']
        table.insert({'user_id':userid, 'string':string})
    return jsonify({'result':'success'})


if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)