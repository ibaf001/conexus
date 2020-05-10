class Config:
    SECRET_KEY = '850b0126f8f89a2637d77e2d29086569'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'noreply.conexussolution@gmail.com'
    MAIL_PASSWORD = 'lbxwkslobobdhuaw'
    UPLOAD_FOLDER = '/Users/ibafumba/PycharmProjects/uploads'
    #MONGODB_URI = '127.0.0.1/ocm'
    MONGODB_URI = 'mongodb://127.0.0.1/ocm'


class ConfigProd:
    SECRET_KEY = '850b0126f8f89a2637d77e2d29086569'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'noreply.conexussolution@gmail.com'
    MAIL_PASSWORD = 'lbxwkslobobdhuaw'
    UPLOAD_FOLDER = '/Users/ibafumba/PycharmProjects/uploads'
    MONGODB_URI = 'mongodb://heroku_hthgvpvz:mm1bk6q6n12hdepm5d9ga7tvne@ds161159.mlab.com:61159/heroku_hthgvpvz'

