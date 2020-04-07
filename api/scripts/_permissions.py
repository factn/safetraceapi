import requests
import _test_api_utils
import _test_script_utils
BASE_URL = None

def get_all_clients_for_permissions(api_key):
    headers = {
        'api_key': api_key,
    }
    body = { }
    response = requests.get(url=BASE_URL + '/clients', json=body, headers=headers).json()
    '''
    client = {
        display_name: ...,
        client_id: ...,
        bio: ...,
    },
    '''
    _test_api_utils.assert_response_is_not_error(response)
    _test_script_utils.print_obj (response['clients'][0], prefix='CLIENT FOR PERMISSIONS:')
    return response['clients']

def check_permissions (api_key, device_id, client_id):
    headers = { 
        'api_key': api_key
    }
    body = { 
        'device_id': device_id,
        'client_id': client_id
    }
    response = requests.get(url=BASE_URL + '/api/permissions', json=body, headers=headers).json()
    # { has_permissions: boolean whetehr or not has_permissions }
    _test_api_utils.assert_response_is_not_error (response)
    return response['has_permissions']

def grant_permission (api_key, device_id, client_id, device_key, print_prefix):
    headers = { 
        'api_key': api_key,
        'device_key': device_key
    }
    body = { 
        'device_id': device_id,
        'client_id': client_id
    }
    response = requests.post(url=BASE_URL + '/api/permissions', json=body, headers=headers).json()
    # { message: 'Permissions Granted For End Party' }
    _test_api_utils.assert_and_print_response(response, print_prefix)
    
def deny_permissions (api_key, device_id, client_id, print_prefix):
    headers = { 
        'api_key': api_key
    }
    body = { 
        'device_id': device_id,
        'client_id': client_id
    }    
    response = requests.delete(url=BASE_URL + '/api/permissions', json=body, headers=headers).json()
    # { message: 'Permissions Denied For End Party' }
    _test_api_utils.assert_and_print_response (response, print_prefix)  