from pymongo import MongoClient
from sshtunnel import SSHTunnelForwarder


# server = SSHTunnelForwarder(
#     '10.0.0.141',  # mongo host
#     ssh_username='ibo',
#     ssh_password='johanna14',
#     remote_bind_address=('127.0.0.1', 27017)
# )
#
# server.start()
# client = MongoClient('127.0.0.1', server.local_bind_port)
# db = client['ocm']
# collection = db["projects"]
#
# # results = collection.find({"name": "gabriel"})
# results = collection.find({})
# # results = collection.delete_one({"id": 1})
#
# for result in results:
#     print(result)
#
#
#
#
# client.close()
# server.stop()


def saveObj(obj):
    server = SSHTunnelForwarder(
        '10.0.0.141',  # mongo host
        ssh_username='ibo',
        ssh_password='johanna14',
        remote_bind_address=('127.0.0.1', 27017)
    )
    server.start()
    client = MongoClient('127.0.0.1', server.local_bind_port)
    db = client['ocm']
    db.projects.save(obj)

    client.close()
    server.stop()


def retrieve_project_by_id(user_id):
    server = SSHTunnelForwarder(
        '10.0.0.141',  # mongo host
        ssh_username='ibo',
        ssh_password='johanna14',
        remote_bind_address=('127.0.0.1', 27017)
    )
    server.start()
    client = MongoClient('127.0.0.1', server.local_bind_port)
    db = client['ocm']
    collections = db["projects"]
    results = collections.find({"user_id": user_id})
    projects = list()
    for result in results:
        projects.append(result)

    client.close()
    server.stop()
    return projects


def remove_project(cl, case):
    server = SSHTunnelForwarder(
        '10.0.0.141',  # mongo host
        ssh_username='ibo',
        ssh_password='johanna14',
        remote_bind_address=('127.0.0.1', 27017)
    )
    server.start()
    client = MongoClient('127.0.0.1', server.local_bind_port)
    db = client['ocm']
    db.projects.remove({'client': cl, 'case': case})

    client.close()
    server.stop()
