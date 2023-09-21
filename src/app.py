from flask import Flask, render_template, request, redirect, url_for, flash
from config import config
from flask_mysqldb import MySQL

#Carpetamodels:
from models.ModelUser import ModelUser

#entities:
from models.entities.User import User
app=Flask(__name__)

db=MySQL(app)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET','POST'])
def signup_create():
    username = request.form.get('username')
    fullname = request.form.get('fullname')
    password = request.form.get('password')
    user = User(username,password,fullname)

    if ModelUser.verificaruario(user, db) != None:
        flash('Usario existe, vuelva a registrarse o inicie sesion')
        return redirect(url_for('signup_create'))
    else:
        try:
            cursor =db.connection.cursor()
            sql="""NSERT INTO `getinfo`.`usuario` (`username`, `password`, `fullname`)
             VALUES ('{}', '{}', '{}')""".format(user.username, User.generar_hash(password) ,user.fullname)
            cursor.execute(sql)
            cursor.close()
        except Exception as ex:
            raise Exception(ex)
        ModelUser.newuser(user,db)
        return redirect (url_for('login'))
 
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        
        #print(request.form['username'])
        #print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user:
                return redirect(url_for('vcpregunta'))
            else:
                flash("contraseña incorrecta...")
            return render_template ('auth/login.html')
        else:
            flash("Usuario no existente...")
            return render_template ('auth/login.html')

        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/vcpregunta')
def vcpregunta():
    return render_template('auth/vcpregunta.html')
        

if __name__=='__main__':
    app.config.from_object(config['development'])
    app.run()

    