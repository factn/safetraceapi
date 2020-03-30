'''
print helpers for the api test
'''

from __future__ import print_function
import json
import os

def print_element (e, indent, prefix, print_normal):
    if (e is None):
        return
    if (isinstance(e, list)):
        print_array(e, indent+1, prefix)
    elif (isinstance(e, dict)):
        print_obj(e, indent+1, prefix)
    else:
        print_normal()

def print_array(a, indent=0, prefix=''):
    print ('   ' * (indent) + prefix + '[')
    for e in a:
        print_element(e, indent, '', lambda: print('   ' * (indent+1) + '{},'.format(str(e))))
    print ('   ' * (indent) + '],')
    
def print_obj (obj, indent=0, prefix=''):
    print ('   ' * (indent) + prefix + '{')
    for key, value in obj.items():
        print_element (value, indent, str(key) + ": ", lambda: print('   ' * (indent+1) + '{}: {},'.format(str(key), str(value))))
    print ('   ' * (indent) + '},')

def print_obj_simple (obj):
    print (json.dumps(obj))

def get_unlocker_keys_to_bypass_rate_limits ():
    with open('RestAPI/.env') as f:
        lines = [l.rstrip() for l in f]
    for l in lines:
        if l.startswith('ST_UNLOCKER_KEY'):
            unlocker_key = l.split('=')[1]
        elif l.startswith('ST_UNLOCKER'):
            unlocker = l.split('=')[1]
    return unlocker_key, unlocker


def get_connect_to_database_cmd (local):
    if local:
        return 'psql -d safetrace_api -U safetrace_user'
    else:
        return 'heroku pg:psql'

def clear_database (local):
    print ('\nCLEARING DATABASE:')
    os.system('cat RestAPI/scripts/initializeDB.sql | ' + get_connect_to_database_cmd(local))

def print_all_users (local):
    print ('\nUSERS:')
    os.system('echo "SELECT * FROM users;" | ' + get_connect_to_database_cmd(local))
def print_all_devices (local):
    print ('\nDEVICES:')
    os.system('echo "SELECT * FROM devices;" | ' + get_connect_to_database_cmd(local))
