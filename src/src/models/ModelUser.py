from .entities.User import User
from werkzeug.security import check_password_hash, generate_password_hash


class ModelUser():

    # lo que hace este metodo es ver si existe en la tabla soporte el usuario
    # que ingreso si esta devuelve un numero mayor a cero, es decir, true
    # y sino false 
    @classmethod
    def es_soporte(self, username, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT COUNT(*) FROM soportet WHERE username = %s"
            cursor.execute(sql, (username,))
            count = cursor.fetchone()[0]
            cursor.close()
            
            return count > 0
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login_user(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql= """SELECT id, username, password, fullname FROM usuario
             WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2],user.password), row[3],"usuario")
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def login_soporte(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql= """SELECT idsoportet, username, password, fullname, esadmi FROM soportet
             WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2],user.password), row[3],"soporte", row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def es_usuario(cls,username,db ):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT COUNT(*) FROM usuario WHERE username = %s"
            cursor.execute(sql, (username,))
            count = cursor.fetchone()[0]
            cursor.close()
            
            return count > 0
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crear_usuario(cls, user, db):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO `getinfo`.`usuario` (`username`, `password`, `fullname`)
                    VALUES ('{}', '{}', '{}')""".format(user.username, user.password, user.fullname)
            cursor.execute(sql)
            cursor.close()
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crear_soporte(cls, user, db):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO `getinfo`.`soportet` (`username`, `password`, `fullname`, `esadmi`)
                    VALUES ('{}', '{}', '{}', '{}')""".format(user.username, user.password, user.fullname, user.esadmi)
            cursor.execute(sql)
            cursor.close()
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(cls, db, id, role):
        try:
            if role == "usuario":
                cursor = db.connection.cursor()
                sql = """SELECT id, username, fullname FROM usuario WHERE id= {} """.format(id)
                cursor.execute(sql)
                row = cursor.fetchone()
                if row != None:
                    return User(row[0], row[1], None, row[2], role)
                else : 
                    return None
                cursor.close()
            else:
                if role == "soporte":
                    cursor = db.connection.cursor()
                    sql = """SELECT idsoportet, username, fullname, esadmi FROM soportet WHERE idsoportet= {} """.format(id)
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    if row != None:
                        return User(row[0], row[1], None, row[2], role, row[3])
                    else : 
                        return None
                    cursor.close()
                else:
                    print(id, role)
            
        except Exception as ex:
            raise Exception(ex)
    
