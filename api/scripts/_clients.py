import requests
import _test_api_utils
import _test_script_utils

BASE_URL = None

def register_client (email, password, name, bio):
    # first obtain keys
    response = requests.get(url=BASE_URL + '/api/encryption', json={}, headers={}).json()
    '''
    response = {
        private_key:    < private key >
        public_key:     < public key >
    },
    '''
    _test_api_utils.assert_response_is_not_error(response)
    _test_script_utils.print_obj (response)
    client = {
        'name': name,
        'email': email,
        'password': password,
        'private_key': response['private_key']
    }

    # pretend we're an app developer signing up
    headers = { 
        'email': email,
        'password': password
    }
    body = {
        'bio': bio,
        'display_name': name,
        'public_key': response['public_key']
    }
    response = requests.post(url=BASE_URL + '/clients', json=body, headers=headers).json()
    _test_api_utils.assert_response_is_not_error(response)
    _test_script_utils.print_obj (response)
    '''
    response = {
        message:    `Account Created For: < email >, save the API and Private Keys included in this object. Make sure to keep them private and secure`,
        api_key:    < api key >,
    },
    '''
    # get the API Key for the app dev
    client['api_key'] = response['api_key']
    return client
    
def register_test_clients ():
    print ('\nCLIENTS SIGN UP:')
    safetrace_client = _test_script_utils.create_safetrace_client()
    client_1 = register_client('email1@site.com', 'password1', 'Client 1', 'some client')
    return [ safetrace_client, client_1 ]

def update_client_credentials(client):
    new_email = 'new_email@site.com'
    new_password = 'new_password'
    headers = { 
        'email': client['email'],
        'password': client['password'],
    }
    body = { 
        'new_email': new_email,
        'new_password': new_password,
    }
    response = requests.patch(url=BASE_URL + '/clients', json=body, headers=headers).json()
    # { "message": "Account Credentials Updated For: some_dev2@site.com" }
    _test_api_utils.assert_and_print_response (response, 'CLIENT CREDENTIALS UPDATE:')
    
    client['email'] = new_email
    client['password'] = new_password
    return client

def client_lose_and_recover_keys (client):
    client['api_key'] = None #uh oh, lost the api keys....
    
    headers = { 
        'email': client['email'],
        'password': client['password'],
    }
    response = requests.get(url=BASE_URL + '/clients/keys', json={}, headers=headers).json()
    _test_api_utils.assert_response_is_not_error(response)
    _test_script_utils.print_obj (response, prefix='RECOVER API AND PRIVATE KEYS:')
    
    client['api_key'] = response['api_key']
    return client

def delete_client_account (client):
    header = { 
        'email': client['email'],
        'password': client['password'],
    }
    response = requests.delete(url=BASE_URL + '/clients', json={}, headers=header).json()
    # { message: 'Client Account Deleted: < email >' }
    _test_api_utils.assert_and_print_response (response, '\nDELETE CLIENT ACCOUNT:')
    return None
