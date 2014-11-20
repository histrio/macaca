"""
File: alfa.py
Author: Rinat F Sabitov
Description:
"""

import logging
import re
import importlib

from sleekxmpp import ClientXMPP
from redmine import Redmine
from database import User

from macaca.commands import CommandError


class CommandsDispatcher(object):

    _cache = {}

    def __init__(self, redmine_url, project_id, patterns):
        self.patterns = []
        self.redmine_url = redmine_url
        self.project_id = project_id
        for ptrn, callback in patterns:
            pair = (re.compile(ptrn + '[\s]*', re.IGNORECASE),
                self.resolve_callback(callback))
            self.patterns.append(pair)
        helpcmd = re.compile(u'^\!HELP', re.IGNORECASE), self.help_command
        self.patterns.append(helpcmd)

    def get_redmine(self, sender):
        redmine = self._cache.get(sender)
        if redmine is None:
            redmine = Redmine(self.redmine_url)
            redmine.default_project_id = self.project_id
            user = User.get_user_by_jid(sender)
            if user:
                redmine.key = user.key
                self._cache[sender] = redmine
        return redmine

    def help_command(self, sender, *args):
        """'!HELP' - show this message """
        helptext = '\n'.join([cmd.__doc__ or "%s - no docstring" % cmd.__name__ for _, cmd in self.patterns])
        return """`text` - new task \n%s
        """ % helptext

    def resolve_callback(self, callback):
        if callable(callback):
            return callback
        else:
            parts = callback.split('.')
            pkg = importlib.import_module('.'.join(parts[:-1]))
            return getattr(pkg, parts[-1])

    def handle(self, sender, cmd):
        logging.info('RCV: %s' % cmd)
        redmine = self.get_redmine(sender)
        for ptrn, callback in self.patterns:
            match = ptrn.match(cmd)
            if match:
                return callback(redmine, sender, *match.groups())
        else:
            if cmd.startswith('!'):
                raise CommandError(u"Unknown command '%s'\n Use '!help' to get help!" % cmd)
            else:
                return self.resolve_callback('macaca.commands.new_post')(redmine, sender, cmd)


class Service(ClientXMPP):
    def __init__(self, jid, password, dispatcher=None):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

        #self.register_plugin('xep_0071')
        #self.register_plugin('html-im')

        self.dispatcher = dispatcher

    def session_start(self, event):
        self.send_presence()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            body = msg.get('body')
            try:
                sender = msg['from'].jid
                reply = self.dispatcher.handle(sender, body)
                msg = self.Message()
                msg['to'] = sender
                msg['body'] = reply['plain']
                msg['type'] = 'chat'
                msg['html']['body'] = reply['html']
                print msg
                msg.send()
            except CommandError as err:
                msg.reply(u'ERROR: %s' % err).send()


def main(args=None, test=False):
    logging.basicConfig(level=logging.INFO,
        format='%(levelname)-8s %(message)s')

    base_config = {
        'redmine_url': "",
        'service_jid': "",
        'service_password': ""
    }

    import argparse
    parser = argparse.ArgumentParser(description='Jabber bot for Redmine')
    parser.add_argument("project_id", help="project identifier")

    parser.add_argument("--resource", help="resource for jabber")
    args = parser.parse_args()
    project_id = args.project_id

    dispatcher = CommandsDispatcher(base_config['redmine_url'], project_id,
        patterns=(
        (u'^\!register (\w+)$', 'macaca.commands.registration'),
        (u'^\!ping', 'macaca.commands.ping'),

        (u'^\!DL$', 'macaca.commands.delete_last_issue'),
        (u'^\!D [#]?(\d+)', 'macaca.commands.delete_issue'),

        (u'^#(\d+)$', 'macaca.commands.issue'),
        (u'^#(\d+) (\w+)$', 'macaca.commands.comment_issue'),
        (u'^#$', 'macaca.commands.issues_list'),
    ))

    xmpp = Service(
        jid='%s/%s' % (base_config['service_jid'],
            args.resource or project_id,),
        password=base_config['service_password'],
        dispatcher=dispatcher,
    )
    xmpp.connect()
    xmpp.process(block=True)


if __name__ == "__main__":
    main()
