class Config:
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*S^'

class developmentConfig(Config):
    DEBUG=True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin1'
    MYSQL_DB = 'getinfo'
    
config={
    'development':developmentConfig
}