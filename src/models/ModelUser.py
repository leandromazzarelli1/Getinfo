from .entities.User import User
from werkzeug.security import check_password_hash, generate_password_hash

class ModelUser():

    @classmethod
    def login(self,db,user):
        try:
            cursor = db.connection.cursor()
            sql= """SELECT id, username, password, fullname FROM usuario
             WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2],user.password), row[3])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def verificaruario(cls,user,db ):
        try:
            cursor =db.connection.cursor()
            sql="""SELECT username FROM usuario
             WHERE username = '{}' """.format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
        except Exception as ex:
            raise Exception(ex)

   