from pymongo import MongoClient
import smtplib
from flask import current_app
from email.message import EmailMessage
import re


def get_mongodb_client():
    return MongoClient(current_app.config['MONGODB_URI'])


def save_project(obj):
    client = get_mongodb_client()
    db = client.get_database()
    db.projects.save(obj)

    client.close()


def retrieve_project_by_id(user_id):
    client = get_mongodb_client()
    db = client.get_database()
    collections = db["projects"]
    results = collections.find({"user_id": user_id}).sort('created at', -1)
    projects = list()
    for result in results:
        projects.append(result)
    client.close()
    return projects


def search_project(project_nuber):
    client = get_mongodb_client()
    db = client.get_database()
    regex = re.compile(project_nuber, re.IGNORECASE)
    results = db.projects.find({'project': regex}).sort('created at', -1)
    projects = list()
    for result in results:
        projects.append(result)
    client.close()
    return projects


def retrieve_project_by_email(user_id):
    client = get_mongodb_client()
    db = client.get_database()
    collections = db["projects"]
    results = collections.find({"user_id": user_id}).sort('created at', -1)
    projects = list()
    for result in results:
        projects.append(result)

    client.close()
    return projects


def remove_project(case):
    client = get_mongodb_client()
    db = client.get_database()
    db.projects.remove({'project': case})
    client.close()


def delete_client(name):
    client = get_mongodb_client()
    db = client.get_database()
    db.clients.delete_one({'_id': name})
    client.close()


def get_projects_by_project_number(project_number):
    client = get_mongodb_client()
    db = client.get_database()
    result = db.projects.find_one({"project": project_number})
    client.close()
    return result


def update_project(obj, project_number):
    client = get_mongodb_client()
    db = client.get_database()
    db.projects.update({'project': project_number}, {'$set': obj})
    client.close()


def get_client_by_id(id):
    client = get_mongodb_client()
    db = client.get_database()
    result = db.clients.find_one({"_id": id})
    client.close()
    return result


def get_clients():
    client = get_mongodb_client()
    db = client.get_database()
    results = db.clients.find({})
    lst = []
    for r in results:
        lst.append(r['_id'])
    client.close()
    return lst


def get_all_projects():
    client = get_mongodb_client()
    db = client.get_database()
    results = db.projects.find({}).sort('created at', -1)
    lst = []
    for r in results:
        lst.append(r)
    client.close()
    return lst


def save_client(obj):
    client = get_mongodb_client()
    db = client.get_database()
    db.clients.save(obj)
    client.close()


def is_csv_file(filename):
    return filename.split('.')[-1] == 'csv'


def get_csv_filename(csvfile):
    pos = csvfile.index('.')
    return csvfile[0:pos]


def create_fields(df):
    df.fillna('', inplace=True)
    d = dict()
    for r in range(len(df)):
        d[df.loc[r, 'field name']] = [df.loc[r, 'type'], df.loc[r, 'field name'], bool(df.loc[r, 'required']),
                                      df.loc[r, 'values']]
    return d


def get_projects_count():
    client = get_mongodb_client()
    db = client.get_database()
    results = db.projects.find({})
    d = {}
    for r in results:
        if r['client'] not in d:
            d[r['client']] = 1
        else:
            d[r['client']] += 1
    client.close()
    return d


def get_projects_for(client_name):
    client = get_mongodb_client()
    db = client.get_database()
    results = db.projects.find({'client': client_name})
    r = list()
    for proj in results:
        r.append(proj)
    client.close()
    return r


def send_email(receiver, case_no):
    try:
        msg = EmailMessage()
        msg["subject"] = 'Assignment for Project'
        msg['From'] = current_app.config['MAIL_USERNAME']
        msg['To'] = receiver
        msg.set_content(f'You have been assigned project {case_no}')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            smtp.send_message(msg)
        return True
    except:
        return False


def send_message(form):
    try:
        msg = EmailMessage()
        msg["subject"] = form.subject.data
        msg['From'] = current_app.config['MAIL_USERNAME']
        msg['To'] = 'blaise.mpinga@conexussolution.com'
        msg.set_content(f'Sender Email: {form.email.data} \n Sender Message: {form.message.data}')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            smtp.send_message(msg)
        return True
    except Exception as e:
        return False
