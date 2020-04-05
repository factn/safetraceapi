import _test_api_utils
import _test_script_utils
import requests

BASE_URL = None

def register_device (api_key, device_id, do_print):
    headers = { 
        'api_key': api_key 
    }
    body = { 
        'device_id': device_id 
    }
    response = requests.post(url=BASE_URL + '/api/devices', json=body, headers=headers).json()
    '''
    response = { 
        message: 'Success! Device Registered. Save the "device_key" included in this object securely, it can only be supplied once!',
        device_key: deviceKey
    }
    '''
    _test_api_utils.assert_response_is_not_error(response)
    if do_print:
        _test_script_utils.print_obj (response)
    return response['device_key']
    
def check_device_registration (api_key, device_id):
    headers = { 
        'api_key': api_key
    }
    body = { 
        'device_id': device_id 
    }
    response = requests.get(url=BASE_URL + '/api/devices', json=body, headers=headers).json()
    # { registered: boolean whetehr or not registered }
    _test_api_utils.assert_response_is_not_error (response)
    return response['registered']

def device_opt_out (api_key, device_id):
    headers = { 
        'api_key': api_key
    }
    body = { 
        'device_id': device_id 
    }    
    response = requests.delete(url=BASE_URL + '/api/devices', json=body, headers=headers).json()
    # { message: < success message > }
    _test_api_utils.assert_and_print_response (response, '\nDEVICE OPT OUT:')    