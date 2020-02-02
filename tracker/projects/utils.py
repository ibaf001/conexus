from pymongo import MongoClient
import smtplib
from email.message import EmailMessage


def save_project(obj):
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    db.projects.save(obj)

    client.close()


def retrieve_project_by_id(user_id):
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    collections = db["projects"]
    results = collections.find({"user_id": user_id}).sort('created_at', -1)
    projects = list()
    for result in results:
        projects.append(result)

    client.close()
    return projects


def retrieve_project_by_email(user_id):
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    collections = db["projects"]
    results = collections.find({"user_id": user_id}).sort('created_at', -1)
    projects = list()
    for result in results:
        projects.append(result)

    client.close()
    return projects


def remove_project(case):
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    db.projects.remove({'case': case})
    client.close()


def get_projects_by_project_number(project_number):
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    result = db.projects.find_one({"Project #": project_number})
    client.close()
    return result


def get_client_by_id(id):
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    result = db.clients.find_one({"_id": id})
    client.close()
    return result

def get_clients():
    client = MongoClient('127.0.0.1', 27017)
    db = client['ocm']
    results = db.clients.find({})
    lst = []
    for r in results:
        lst.append(r['_id'])
    return lst





def send_email(receiver, case_no):
    try:
        msg = EmailMessage()
        msg["subject"] = 'Assignment for Project'
        msg['From'] = 'mbolokwa@gmail.com'
        msg['To'] = receiver
        msg.set_content(f'You have been assigned project {case_no}')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('mbolokwa@gmail.com', 'johanna@14')
            smtp.send_message(msg)
        return True
    except:
        return False
