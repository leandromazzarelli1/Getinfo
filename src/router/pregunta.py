from flask import Blueprint, render_template, request, current_app, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models.ModelUser import ModelUser
from utils.utils import roles_required
from datetime import datetime

pregunta = Blueprint('pregunta', __name__)


@pregunta.route('/vcpregunta', methods = ['POST','GET'])
@login_required
def vcpregunta():
    db = current_app.db 
    user_id = current_user.id
    
    if request.method == 'POST':
        problema = request.form['problema']
        current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor = db.connection.cursor()
        sql = """INSERT INTO `getinfo`.`pregunta` (`descripcion`,`idusuario`,`fecha`,`respondido`) VALUES
        ('{}','{}','{}','{}')""".format(problema, user_id, current_date_time, 0)
        cursor.execute(sql)
        cursor.close()
        db.connection.commit()
        print(problema)
        return render_template('auth/vcpregunta.html')
    else:
        return render_template('auth/vcpregunta.html')
    
@pregunta.route('/vspregunta', methods = ['POST','GET'])
@login_required
@roles_required(['soporte'])
def vspregunta():
    db = current_app.db 
    user_id = current_user.id
    preguntas = []  # Lista para almacenar las preguntas
    norespondido = 0
    
    try:
        cursor = db.connection.cursor()
        sql = """SELECT idpregunta, fecha, descripcion FROM pregunta WHERE respondido = '{}'""".format(norespondido)
        cursor.execute(sql)
        preguntas = cursor.fetchall()  # Obtener todas las filas de la consulta
    except Exception as ex:
        raise Exception(ex)

    return render_template('auth/vspregunta.html', preguntas=preguntas)


@pregunta.route('/respuesta', methods = ['POST'])
@login_required
@roles_required(['soporte'])
def respuesta():
    if request.method == 'POST':    
        db = current_app.db
        idpregunta = request.json.get('pregunta_id')
        respuesta = request.json.get('respuesta')
        idsoporte = current_user.id

        cursor = db.connection.cursor()
        sql = """INSERT INTO `getinfo`.`respuesta` (`descripcion`,`idpregunta`,`idsoportet`) VALUES
        ('{}','{}','{}')""".format(respuesta, idpregunta, idsoporte)
        print("el id es: ", idpregunta, "y la respuesta es: ", respuesta, "y el id del usuario actual es: ", idsoporte)
        cursor.execute(sql)
        cursor.close()
        db.connection.commit()

        respondido = 1

        cursor = db.connection.cursor()
        segundosql = """UPDATE pregunta SET respondido = ('{}') WHERE idpregunta = ('{}')""".format(respondido, idpregunta)
        cursor.execute(segundosql)
        cursor.close()
        db.connection.commit()

        return jsonify({'message': 'Respuesta recibida con éxito'})

    return jsonify({'error': 'Error al procesar la solicitud'})

@pregunta.route('/vcrespuesta', methods=['POST', 'GET'])
@login_required
def vcrespuesta():
    
    db = current_app.db
    cursor = db.connection.cursor()
    sql = """SELECT r.idrespuesta, r.descripcion, r.idsoportet, s.fullname
                FROM respuesta AS r
                INNER JOIN soportet AS s ON r.idsoportet = s.idsoportet"""
    cursor.execute(sql)
    respuestas = cursor.fetchall()
    cursor.close()
     # Verifica que los datos se impriman correctamente en la consola
    # También puedes usar logging para registrar los datos
    
    return render_template('auth/vcrespuesta.html', respuestas=respuestas)

@pregunta.route('/calificar', methods=['POST'])
@login_required
def calificar():
    if request.method == 'POST':
        idusuario = current_user.id
        formData = request.json 
        puntuacion = None
        for data in formData:
            
            if data['name'] == 'puntuacion':
                puntuacion = data['value']
        # Procesar y guardar los datos en la base de datos (Asegúrate de hacer esto de forma segura)
        db = current_app.db
        cursor = db.connection.cursor()
        sql = """INSERT INTO calificacion (idusuario, punto) VALUES (%s, %s)"""
        cursor.execute(sql, (idusuario, puntuacion))
        db.connection.commit()
        cursor.close()

        return jsonify({'message': 'Calificación recibida con éxito'})

    return jsonify({'error': 'Error al procesar la solicitud'})