from flask import Flask, render_template, redirect, url_for,request, session, g
from flask_pymongo import PyMongo

app = Flask(__name__, static_url_path='/static')
mongo = PyMongo(app,uri="mongodb://127.0.0.1:27017/User")
app.secret_key ="fghgfda"


@app.before_request
def before_request():
    g.user = None
    if 'User' in session:
        g.user = session['User']


@app.route('/', methods=['POST','GET'])
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        name1 = request.form.get('name1')
        name2 = request.form.get('name2')
        userEmail = request.form.get('userEmail')
        dob = request.form.get('dob')
        telno = request.form.get('telNo') 

        if username == '' or password1 == ''or password2 == '' or name1 == ''or name2 == ''or userEmail == ''or dob == ''or telno == '':
            error ="Please enter all the credentials!"
            return render_template('Signup.html',error=error)
        
        elif password1 != password2:
            error ="ERROR PASSWORD DOESN'T MATCH !"
            return render_template('Signup.html',error=error)
        
        else:
            mongo.db.project_collection.insert_one({
                "username": username,
                "password": password1,
                "firstname": name1,
                "surname": name2,
                "userEmail": userEmail,
                "dob": dob,
                "telno": telno
            })
            return redirect(url_for('login'))

    return render_template('Signup.html')


@app.route('/mainpage', methods =['POST','GET'])
def mainpage():
    if g.user:
        return render_template("mainpage.html")
    else:
         return redirect (url_for('login'))
        
    
@app.route('/logout')
def logout():
    session.pop('User',None)
    return  redirect(url_for('login'))
      
        
@app.route('/login', methods=['POST','GET'])
def login():
    pwd=''
    users = mongo.db.project_collection.find()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == '' or password == '':
            error ="Please enter all the credentials!"
            return render_template('Login.html', error=error)
        else:
            for user in users:
                if user['username'] == username:
                    pwd = user['password']
            if pwd == '':
                error ="User not found!"
                return render_template('Login.html', error=error)
            elif pwd == password:
                session["User"] = username
                return redirect(url_for('mainpage'))
            else:
                error ="Incorrect Password!!"
                return render_template('Login.html', error=error)  
    return render_template('Login.html')

@app.route('/school')
def school():
        return render_template("school.html")



if __name__ == "__main__":
    app.run(debug=True)