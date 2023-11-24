from flask import Flask, render_template, request, redirect, url_for, flash, current_app, session
from config import config
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user
from router.pregunta import pregunta
from router.soporte import soporte
from utils.utils import roles_required
from flask_login import current_user

#Carpetamodels:
from models.ModelUser import ModelUser

#entities:
from models.entities.User import User

app = Flask(__name__)

csrf=CSRFProtect()
db=MySQL(app)
login_manager_app = LoginManager(app)

with app.app_context():
    current_app.db = db

@login_manager_app.user_loader
def load_user(id):
    user_role = session.get('role')
    print ("en el load user", user_role)
    return ModelUser.get_by_id(db, id, user_role)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/signup', methods=['POST', 'GET'])
def signup_create():
    if request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        password = request.form.get('password')

        if username is None:
            flash('Nombre de usuario vacio', 'danger')
            return redirect(url_for('signup_create'))

        if password is None:
            flash('Contraseña no proporcionada', 'danger')
            return redirect(url_for('signup_create'))

        if len(username) > 255:
            flash('Nombre de usuario demasiado largo', 'danger')
            return redirect(url_for('signup_create'))

        if ModelUser.es_usuario(username, db):
            flash('Usuario existe, vuelva a registrarse o inicie sesión', 'danger')
            return redirect(url_for('signup_create'))
        else:
            if ModelUser.es_soporte(username, db):
                flash ('Usuario existe, vuelva a registrarse o inicie sesión', 'danger')
                return redirect(url_for('signup_create'))
            else:    
                password_hash = User.generar_hash(password)
                user = User(0, username, password_hash, fullname)
                ModelUser.crear_usuario(user, db)
                flash ('Cuenta creada!')
                return redirect(url_for('login'))
                
    return render_template('auth/registro.html')

 
@app.route('/login', methods=['GET','POST'])    
def login():
    if request.method == 'POST':
        user = User(0, request.form['username'], request.form['password'])
        username = request.form['username']
        
        # si es soporte, entonces ira al endpoint correspondiente sino ira al
        # de usuario 
        if ModelUser.es_soporte(username, db):
            logged_user = ModelUser.login_soporte(db, user)

            if logged_user:
                if logged_user.password:
                    login_user(logged_user)
                    session['role']= "soporte"
                    print ("el rol aca es:" + logged_user.role + logged_user.username, "es admi? ", logged_user.esadmi) 
                    return redirect(url_for('pregunta.vspregunta'))  
                else:
                    flash("credenciales incorrectas")
                    return render_template('auth/login.html')
            else:
                flash("credenciales incorrectas")
                return render_template('auth/login.html')
        else:
            logged_user = ModelUser.login_user(db, user)
            if logged_user:
                if logged_user.password:
                    login_user(logged_user)
                    session['role']= "usuario"
                    return redirect(url_for('pregunta.vcpregunta'))
                else:
                    flash("credenciales incorrectas ")
                    return render_template('auth/login.html')
            else:
                flash("credenciales incorrectas ")
                return render_template('auth/login.html')

        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/acceso_denegado')
def acceso_denegado():
    return "Acceso denegado. No tienes permiso para ver esta página."


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1> Página no encontrada </h1>", 404

if __name__=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401,status_401)
    app.register_error_handler(404,status_404)
    app.register_blueprint(pregunta)
    app.register_blueprint(soporte)
    app.run()

