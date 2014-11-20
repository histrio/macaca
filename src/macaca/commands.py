"""
File: alfa.py
Author: Rinat F Sabitov
Email: 0
Github: 0
Description:
"""

from redmine.exceptions import AuthError
from macaca.database import session_scope, User


class CommandError(Exception):
    pass


def registration(redmine, sender, *args):
    """'!REGISTER <api_key>' - register new api key.
    You can get your key from /my/account"""
    try:
        key, = args
    except ValueError as er:
        raise CommandError('Invalid arguments `%s` count: %s' % (args, er))

    redmine.key = key
    with session_scope() as session:
        try:
            ruser = redmine.user.get('current')
        except AuthError as err:
            raise CommandError('Registration error: %s' % err)

        if not ruser:
            raise CommandError('Unknown user')
        else:
            user = User(
                jid=sender,
                name=ruser.mail,
                fullname=' '.join([ruser.lastname or '', ruser.firstname or '']),
                external_id=ruser.id,
                key=key)
            session.add(user)
            return "%s registered" % user


def authorized(clb):

    def wrapper(redmine, sender, *args, **kwargs):
        user = User.get_user_by_jid(sender)
        if user is None:
            raise CommandError(u"User '%s' not registered" % sender)
        return clb(redmine, sender, *args, **kwargs)

    return wrapper


IM_LAST_COMMENTS, IM_ALL_COMMENTS = range(1,3)


import urllib
def xmpp(*dargs):

    def decorator(clb):

        def wrapper(*args, **kwargs):
            result = clb(*args, **kwargs)

            cmd_list = []

            quoted_id = urllib.quote('#%d' % result['id'])

            if IM_LAST_COMMENTS in dargs:
                cmd = '<a href="xmpp:forepk@portal.bars-open.ru/test?message;body={0} +">[+]</a>'.format(quoted_id)
                cmd_list.append(cmd)
            if IM_ALL_COMMENTS in dargs:
                cmd = '<a href="xmpp:forepk@portal.bars-open.ru/test?message;body={0} ++">[++]</a>'.format(quoted_id)
                cmd_list.append(cmd)

            issue_link = '<a href="xmpp:forepk@portal.bars-open.ru/test?message;body={0} ">#{1}</a>'.format(quoted_id, result['id'])
            result['html'] = "<div><div>{0}</div><div>{1} {2}</div></div>".format(result['plain'], issue_link, ''.join(cmd_list))
            return result
        return wrapper

    return decorator



@authorized
@xmpp(IM_LAST_COMMENTS, IM_ALL_COMMENTS)
def new_post(redmine, sender, *args):
    task_description, = subject, = args
    if len(task_description) > 40:
        subject = ' '.join(task_description.split(' ')[:5]) + '...'
    issue = redmine.issue.create(
        project_id='test',
        subject=subject,
        description=task_description
    )
    return {"id": issue.id, "plain": 'Issue #%d is created' % issue.id}


def ping(sender, *args):
    """'!PING' - Pong """
    return "PONG"


@authorized
def delete_last_issue(redmine, sender, *args):
    """'!DL' - delete last created task"""
    user = User.get_user_by_jid(sender)
    last_issue, = redmine.issue.filter(
        project_id=redmine.default_project_id,
        author_id=user.external_id,
        limit=1,
        sort="created_on:desc"
    )
    redmine.issue.delete(last_issue.id)
    return u'Task #%s deleted' % last_issue.id


def delete_issue(redmine, sender, *args):
    """'!D #task_id' - delete task"""
    _id, = args
    redmine.issue.delete(_id)
    return u'Task #%s deleted' % _id


def issues_list(redmine, sender, *args):
    """'#' - show last tasks"""
    user = User.get_user_by_jid(sender)
    issues = redmine.issue.filter(
        project_id=redmine.default_project_id,
        assigned_to_id=user.external_id,
        limit=8,
    )
    return '\n'.join(map(lambda rec: "#%d %s" % (rec.id, rec.subject),
        issues))


def issue(redmine, sender, *args):
    _id, = args
    issue = redmine.issue.get(_id)
    return """'%s'
    %s
    """ % (issue.subject, issue.description)


def comment_issue(redmine, sender, *args):
    _id, comment, = args
    redmine.issue.update(_id, notes=comment)
    return u'Comment added'
