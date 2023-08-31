from flask import Flask, render_template, request, redirect, url_for
from config import config
from flask_mysqldb import MySQL

app=Flask(__name__)

db=MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))
 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db,user)

        if logged_user != None:
            if logged_user.password:
                return redirect(url_for('perfilcliente'))
            else:
                flash("Credenciales incorrectas...")
            return render_template ('auth/login.html')
        else:
            flash("Usuario no existente...")
            return render_template ('auth/login.html')

        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
        

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()