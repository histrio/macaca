#"""
#File: test_macaca.py
#Author: Rinat F Sabitov
#Email: 0
#Github: 0
#Description:
#"""

#import os
#import sys
#import unittest
#import pytest

#root_dir = os.path.dirname(__file__)
#sys.path.insert(0, os.path.join(root_dir, '../src'))

#from macaca import alfa, commands
#from macaca.database import init_database, drop_database


#def setup_function(fun):
    #init_database()


#def teawrdown_function(fun):
    #drop_database()


#class RedmineDummy():

    #def get_current_user_info(self, key):
        #return {'user':{}}


#def test_empty_dispatcher():
    #redmine = RedmineDummy()
    #dispatcher = alfa.CommandsDispatcher(redmine,{})
    #assert dispatcher.help_command(redmine, None, None)
    #assert dispatcher.handle(None, "!HELP")
    #assert dispatcher.handle(None, "!help")
    #assert dispatcher.handle(None, "!help random stuff")


#def test_registration_command():
    #redmine = RedmineDummy()
    #commands.registration(redmine, 'test@test', 'test')


#if __name__ == '__main__':
    #unittest.main()
