"""
File: tasks.py
Author: Rinat F Sabitov
Description:
"""

from celery import Celery
from redmine import Redmine
app = Celery('tasks', broker='redis://127.0.0.1:6379/0')


def get_redmie_connection(user):
    """ Создаем для пользователя объект для работы с редмайном.
    Каждый раз, да.
    """
    redmine = Redmine('http://task.bars-open.ru/', key=user.key)
    return redmine

@app.task
def create_new_issue(user, body):
    redmine = get_redmie_connection(user)
    redmine.issue.create(body)
