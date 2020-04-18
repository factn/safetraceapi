'''
    script to test the api endpoints
'''
from __future__ import print_function
import sys
import math
import datetime as dt
import time
import requests
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

def connect_to_db_cmd (local):
    return 'psql -d safetrace_api -U safetrace_user' if local else 'heroku pg:psql --app safetraceapi'

def clear_database (local):
    print ('\nCLEARING DATABASE:')
    os.system('cat api/scripts/initializeDB.sql | ' + connect_to_db_cmd(local))


def _print_all_table (table, local):
    print ('\n{}:'.format(table.upper()))
    os.system('echo "SELECT * FROM {};" | '.format(table) + connect_to_db_cmd(local))


def print_all_triples (local):
    _print_all_table ('triples', local)
def print_all_shares (local):
    _print_all_table ('shares', local)
def print_all_results (local):
    _print_all_table ('results', local)


def get_safetrace_key ():
    with open('api/.env') as f:
        lines = [l.rstrip() for l in f]
    for l in lines:
        if l.startswith('SAFETRACE_API_KEY'):
            return l.split('=')[1]
        

def assert_and_print_response (response):
    assert not 'error' in response, response['error']
    print_obj (response)


LOCAL = True
BASE_URL = 'http://localhost:3000' if LOCAL else 'https://safetraceapi.herokuapp.com'

try:
    '''CLEAR THE DATABASE '''
    clear_database(LOCAL)

    print_all_results(LOCAL)
    print_all_shares(LOCAL)
    print_all_triples(LOCAL)

    headers = { 
        'api_key': get_safetrace_key() 
    }


    print('Getting Nodes:')
    response = requests.get(url=BASE_URL + '/api/nodes', json={ }, headers=headers).json()
    '''
    response = {
        nodes: [
            {
                node_id: integer,
                public_key: string,
            },
            { ... },
            { ... },
        ]
    }
    '''
    assert_and_print_response (response)
    
    all_nodes = response['nodes']

    assert len(all_nodes) > 0, 'Forgot to add MPC Nodes'

    '''
    Simulate posting and getting triples
    '''

    node_id_to_use = all_nodes[0]['node_id']
    print('Posting Triple:')
    body = { 
        'node_id': node_id_to_use,
        'triple_id': 'some triple ID',
        'share': 'the triple share...'
    }
    response = requests.post(url=BASE_URL + '/api/triples', json=body, headers=headers).json()
    assert_and_print_response (response)
    '''
    response = { 
        status: OK
    }
    '''
    print_all_triples(LOCAL)


    print('Getting Triple:')
    body = { 
        'node_id': node_id_to_use,
        'triple_id': 'some triple ID',
    }
    response = requests.get(url=BASE_URL + '/api/triples', json=body, headers=headers).json()
    assert_and_print_response (response)
    '''
    response = { 
        share: share string
    }
    '''
    print_all_triples(LOCAL)


    '''
    POST SHARES (for each node)
    '''
    print('Posting Shares')
    body = { 
        'shares': [ { 
            'node_id': n['node_id'],
            'share': 'share_for_nodeID: {}'.format(n['node_id'])
        } for n in all_nodes ]
    }
    response = requests.post(url=BASE_URL + '/api/shares', json=body, headers=headers).json()
    '''
    response = { 
        status: "OK"
    }
    '''
    assert_and_print_response (response)
    
    print_all_shares(LOCAL)

    print('Waiting Until Next Hour To MPC Get')
    print('')
    time_posted = dt.datetime.utcnow()

    # minute = math.floor(time_posted.minute / 10) * 10
    # computation_id_when_posted = '{}:{}-{}/{}/{}'.format(time_posted.hour, minute if minute >= 10 else '0' + str(minute), time_posted.month, time_posted.day, time_posted.year)

    computation_id_when_posted = '{}-{}/{}/{}'.format(time_posted.hour, time_posted.month, time_posted.day, time_posted.year)

    delta = dt.timedelta(hours=1)
    # delta = dt.timedelta(minutes=10)
    
    # 2 minute buffer to make sure computation id for mpc getting shares is teh one form the posts before
    clients_post_end_time = (time_posted + delta).replace(microsecond=0, second=0, minute=2) 
    # clients_post_end_time = (time_posted + delta).replace(microsecond=0, second=0)

    while True:
        # Wait for 5 seconds
        time.sleep(1)

        cur_time = dt.datetime.utcnow()
        
        sys.stdout.write('\rSeconds Until Next Computation ID: ' + str((clients_post_end_time - cur_time).seconds) + '----------')
        sys.stdout.flush()

        if cur_time > clients_post_end_time:
            print('\n')
            break
            
    
    '''
    simulate computation for each node
    '''
    for n in all_nodes:

        print('Getting Shares For Node ID: ' + str(n['node_id']))
        body = { 
            'node_id': n['node_id']
        }
        response = requests.get(url=BASE_URL + '/api/shares', json=body, headers=headers).json()
        '''
        response = {
            computation_id: string,
            shares: [
                {
                    device_id: string,
                    share: string
                },
                { ... },
                { ... },
            ]
        }
        '''
        assert_and_print_response (response)
    
        computation_id = response['computation_id']

        '''
        MPC does calculations...
        '''
        print('Posting Results For Node ID: ' + str(n['node_id']))
        
        body = { 
            'node_id': n['node_id'],
            'computation_id': computation_id,
            'shares': [ { 
                'area_id': i,
                'share': 'Result share_for_areaID: {}'.format(i)
            } for i in range(3) ]
        }
        response = requests.post(url=BASE_URL + '/api/results', json=body, headers=headers).json()
        '''
        response {
            status: OK
        }
        '''
        assert_and_print_response (response)
    

    print ('Done With Computations...')

    print_all_results(LOCAL)
    print_all_shares(LOCAL)


    print('Try To Get Result Shares For Computation ID: {}'.format(computation_id_when_posted))
    body = { 
        'computation_id': computation_id_when_posted
    }
    response = requests.get(url=BASE_URL + '/api/results', json=body, headers=headers).json()
    '''
    response {
        shares: [
            {
                node_id: integer,
                area_id: integer,
                share: string
            },
            { ... },
            { ... },
        ]
    }
    '''
    assert_and_print_response (response)
    

finally:
    clear_database(LOCAL)

