from flask import url_for
from flask_mail import Message
from tracker import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@ocmgroup.com',
                  recipients=[user.email])

    msg.body = f'''To reset your password visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email.
    '''

    mail.send(msg)
