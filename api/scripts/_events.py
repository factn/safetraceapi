import requests
import _test_api_utils
import _test_script_utils

BASE_URL = None

# SHOWS HOW TO GET ALL DATA FROM A TABLE
def get_all_events_for_client(client):
    headers = {
        'api_key': client['api_key'],
        'private_key': client['private_key']
    }
    body = {
        'public_key': client['public_key'],
        'columns': 'device_id, row_type, longitude, latitude, contact_id, contact_level, symptoms, infection_status'
    }
    
    response = requests.get(url=BASE_URL + '/api/events', json=body, headers=headers).json()
    # { rows: an array of objects containing a key/value pair for each column requested (all columns if no columns specified) }
    _test_api_utils.assert_response_is_not_error(response)
    return response['rows']

def print_all_events_for_client(client):
    rows = get_all_events_for_client(client)
    
    if len(rows) == 0:
        print ('NO EVENTS FOR ({}):'.format(client['name']))
        return

    print ('\nEVENTS ({}):'.format(client['name']))
    for i in range(len(rows)):
        _test_script_utils.print_obj (rows[i])

def print_all_events_for_clients (clients):
    for client in clients:
        if client:
            print_all_events_for_client(client)

def post_data_row (api_key, device_key, body, do_print):
    if do_print:
        print ('Encrytpted:')
    headers = { 
        'api_key': api_key,
        'device_key': device_key
    }
    response = requests.post(url=BASE_URL + '/api/encryption', json=body, headers=headers).json()
    # { encrypted_body: < an object with all the proper keys encrypted to send to the event data table > }
    _test_api_utils.assert_response_is_not_error(response)
    
    if do_print:
        _test_script_utils.print_obj (response)

    body = response['encrypted_body']

    response = requests.post(url=BASE_URL + '/api/events', json=body, headers=headers).json()
    # { event_id: the event id generated for the POSTed row }
    if do_print:
        _test_api_utils.assert_and_print_response (response, 'Posted:')
    else:
        _test_api_utils.assert_response_is_not_error(response)
