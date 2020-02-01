class Config:
    SECRET_KEY = '850b0126f8f89a2637d77e2d29086569'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mbolokwa@gmail.com'  # todo put in environment variable?
    MAIL_PASSWORD = 'johanna@14'  # todo put in environment variable?
    UPLOAD_FOLDER = '/Users/ibafumba/PycharmProjects/uploads'
