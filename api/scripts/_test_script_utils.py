'''
helpers for the api test script
'''

from __future__ import print_function
import json
import os

def truncate_to_length (value, length = 25):
    s = str(value)
    return s if len(s) <= length else (s[:length] + '...')

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
        print_element(e, indent, '', lambda: print('   ' * (indent+1) + '{},'.format(truncate_to_length (e))))
    print ('   ' * (indent) + '],')
    
def print_obj (obj, indent=0, prefix=''):
    print ('   ' * (indent) + prefix + '{')
    for key, value in obj.items():
        print_element (value, indent, str(key) + ": ", lambda: print('   ' * (indent+1) + '{}: {},'.format(str(key), truncate_to_length (value))))
    print ('   ' * (indent) + '},')

def print_obj_simple (obj, prefix=None):
    print (('' if prefix is None else prefix) + ' ' + (json.dumps(obj)))

def connect_to_db_cmd (local):
    return 'psql -d safetrace_api -U safetrace_user' if local else 'heroku pg:psql'

def clear_database (local):
    print ('\nCLEARING DATABASE:')
    os.system('cat api/scripts/initializeDB.sql | ' + connect_to_db_cmd(local))

def print_all_clients (local):
    print ('\nCLIENTS:')
    os.system('echo "SELECT client_id, display_name, email, bio FROM clients;" | ' + connect_to_db_cmd(local))
    
def print_all_devices (local):
    print ('\nDEVICES:')
    os.system('echo "SELECT SUBSTRING(device_id, 1, 10) "device_id", SUBSTRING(device_key, 1, 10) "device_key" FROM devices;" | ' + connect_to_db_cmd(local))

def print_all_permissions (local):
    print ('\nPERMISSIONS:')
    os.system('echo "SELECT SUBSTRING(device_id, 1, 10) "device_id", client_id, SUBSTRING(device_key, 1, 10) "device_key" FROM ep_permissions;" | ' + connect_to_db_cmd(local))

def get_safetrace_keys ():
    with open('api/.env') as f:
        lines = [l.rstrip() for l in f]
    for l in lines:
        if l.startswith('SAFETRACE_API_KEY'):
            SAFETRACE_API_KEY = l.split('=')[1]
        elif l.startswith('SAFETRACE_PUBLIC_KEY'):
            SAFETRACE_PUBLIC_KEY = l.split('=')[1]
        elif l.startswith('SAFETRACE_PRIVATE_KEY'):
            SAFETRACE_PRIVATE_KEY = l.split('=')[1]
    return SAFETRACE_API_KEY, SAFETRACE_PUBLIC_KEY, SAFETRACE_PRIVATE_KEY

def create_safetrace_client ():
    SAFETRACE_API_KEY, SAFETRACE_PUBLIC_KEY, SAFETRACE_PRIVATE_KEY = get_safetrace_keys()
    return {
        'name': 'SafetraceAPI',
        'api_key': SAFETRACE_API_KEY, 
        'private_key': SAFETRACE_PRIVATE_KEY, 
        'public_key': SAFETRACE_PUBLIC_KEY 
    }