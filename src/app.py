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

@app.route('/signup', methods=['POST', 'GET'])
def signup_create():
    if request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        password = request.form.get('password')

        if password is None:
            flash('Contraseña no proporcionada', 'danger')
            return redirect(url_for('signup_create'))

        password_hash = User.generar_hash(password)
        user = User(0, username, password_hash, fullname)

        if len(user.username) > 255:
            flash('Nombre de usuario demasiado largo', 'danger')
            return redirect(url_for('signup_create'))

        if ModelUser.verificar_usuario(user, db):
            flash('Usuario existe, vuelva a registrarse o inicie sesión', 'danger')
            return redirect(url_for('signup_create'))
        else:
            ModelUser.crear_usuario(user, db)
            return redirect(url_for('login'))
    return render_template('auth/registro.html')

 
@app.route('/login', methods=['GET','POST'])    
def login():
    if request.method == 'POST':
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

    