from flask import Blueprint, render_template, request, current_app, flash, current_app, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.ModelUser import ModelUser
from utils.utils import roles_required
from models.entities.User import User

soporte = Blueprint('soporte',__name__)


@soporte.route('/crear_soporte', methods = ['POST','GET'])
@login_required
@roles_required(['soporte'])
def crear_soporte():
    db = current_app.db 
    if request.method == 'POST':
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        esadmi = 1 if request.form.get('esadmin') == 'si' else 0

        if username is None and password is None and len(username) > 255:
            flash('Nombre de usuario vacio', 'danger')
            return redirect(url_for('crear_soporte'))
        
        if ModelUser.es_usuario(username, db) or ModelUser.es_soporte(username, db):
             flash('Usuario existe, vuelva a registrar', 'danger')
        else:    
            password_hash = User.generar_hash(password)
            user = User(0, username, password_hash, fullname," " ,esadmi)
            ModelUser.crear_soporte(user, db)
            flash('Cuenta creada!')

        return redirect(url_for('soporte.crear_soporte'))
        
    return render_template('auth/crearsoporte.html')

@soporte.route('/obtener_soporte')
@login_required
@roles_required(['soporte'])
def obtener_soporte():
    db = current_app.db 
    user_id = current_user.id
    usuarios_soporte = [] # Obtener los usuarios de soporte
    
    try:
        cursor = db.connection.cursor()
        sql = """SELECT idsoportet, fullname, username, esadmi FROM soportet WHERE idsoportet != %s"""
        cursor.execute(sql, (user_id,))
        usuarios_soporte = cursor.fetchall()
    except Exception as ex:
        raise Exception(ex)
    return jsonify(usuarios_soporte)

@soporte.route('/contrasena_soporte/<int:usuario_id>', methods=['POST'])
@login_required
@roles_required(['soporte'])
def modificar_soporte(usuario_id):

   if request.method == 'POST':
        db = current_app.db 
        #la nueva contraseña del formulario enviado desde el frontend
        nueva_contrasena = request.json.get('nuevaContrasena')
        contraseña_hash = User.generar_hash(nueva_contrasena)
        try:
            cursor = db.connection.cursor()
            sql = """UPDATE soportet SET password = %s WHERE idsoportet = %s"""
            cursor.execute(sql, (contraseña_hash, usuario_id))
            db.connection.commit()
            cursor.close()
            print("llego a guardarlo creo")
            return jsonify({'message': 'Contraseña actualizada correctamente'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@soporte.route('/eliminar_soporte/<int:usuario_id>', methods=['DELETE'])
@login_required
@roles_required(['soporte'])
def eliminar_soporte(usuario_id):
    if request.method == 'DELETE':
        db = current_app.db 
        print("El usuario a eliminar es:", usuario_id)
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM soportet WHERE idsoportet = %(id)s"
            cursor.execute(sql, {'id': usuario_id})
            db.connection.commit()
            cursor.close()
            print("Usuario eliminado")

            # Obtener la lista actualizada de usuarios de soporte
            sql_get_users = """SELECT idsoportet, fullname, username, esadmi FROM soportet WHERE idsoportet != %s"""
            cursor = db.connection.cursor()
            cursor.execute(sql_get_users, (current_user.id,))
            usuarios_soporte = cursor.fetchall()
            cursor.close()

            # Enviar la lista actualizada como parte de la respuesta JSON
            return jsonify({'message': 'Se ha eliminado al usuario', 'usuarios': usuarios_soporte})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
