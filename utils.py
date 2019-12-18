import smtplib
import os


def send_email():
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login('mbolokwa@gmail.com', 'johanna@14')
    subject = 'message from ibolas'
    body = 'Are you going to Canada ? '
    msg = f'Subject: {subject}\n\n{body}'
    smtp.sendmail('mbolokwa@gmail.com', 'ibobafumba@gmail.com', msg)



