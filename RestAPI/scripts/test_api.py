'''
    script to test the api endpoints
'''

from __future__ import print_function

import test_api_helper
import random
import requests
import json

(unlocker_key, unlocker) = test_api_helper.get_unlocker_keys_to_bypass_rate_limits()
print (unlocker_key + "/" + unlocker)
def build_headers (api_key=None):
    if api_key is None:
        return { unlocker_key: unlocker }
    return { 'x-api-key': api_key, unlocker_key: unlocker }

LOCAL = True

test_api_helper.clear_database(LOCAL)

if LOCAL:
    base_url = 'http://localhost:3000'
else:
    base_url = 'https://safetraceapi.herokuapp.com'

users_url = base_url + '/users'
events_url = base_url + '/api/events'
devices_url = base_url + '/api/devices'

# SHOWS HOW TO GET ALL DATA FROM A TABLE
def print_all_events():
    print ('\nEVENTS:')
    response = requests.get(url=events_url, json={}, headers=build_headers ()).json()
    # { rows: an array of objects containing a key/value pair for each column requested (all columns if no columns specified) }
    
    assert_response_is_not_error(response)
    rows = response['rows']
    for i in range(len(rows)):
        test_api_helper.print_obj (rows[i])

def assert_response_is_not_error (response):
    assert not 'error' in response, response['error']

def assert_and_print_response (response):
    assert_response_is_not_error(response)
    test_api_helper.print_obj_simple (response)

dev_email = 'some_dev@site.com'
dev_password = 'password'
def register_user ():
    print ('\nUSER SIGN UP:')
    # pretend we're an app developer signing up
    body = { 
        'email': dev_email,
        'password': dev_password,
    }
    response = requests.post(url=users_url, json=body, headers=build_headers()).json()
    assert_response_is_not_error(response)
    test_api_helper.print_obj (response)
    '''
    response = {
        message: Account Created For: some_dev@site.com, save the API Key included in this object,
        apiKey: 'xxx-xxxxx-xxxx-xxxxxx',
    },
    '''
    # get the API Key for the app dev
    return response['apiKey']

api_key = register_user()
test_api_helper.print_all_users(LOCAL)

def update_user_credentials():
    print ('\nUSER CREDENTIALS UPDATE:')
    new_dev_email = 'some_dev2@site.com'
    new_dev_password = 'password2'
    body = { 
        'email': dev_email,
        'password': dev_password,
        'newEmail': new_dev_email,
        'newPassword': new_dev_password,
    }
    response = requests.patch(url=users_url, json=body, headers=build_headers()).json()
    # { "message": "Account Credentials Updated For: some_dev2@site.com" }
    assert_and_print_response (response)
    return new_dev_email, new_dev_password

dev_email, dev_password = update_user_credentials()
test_api_helper.print_all_users(LOCAL)

api_key = None #uh oh, lost the api key....

def recover_api_key ():
    print ('\nRECOVER API KEY:')
    body = { 
        'email': dev_email,
        'password': dev_password,
    }
    response = requests.get(url=users_url, json=body, headers=build_headers()).json()
    # { "apiKey": "xxxx-xxx-xxx-xxxx" }
    assert_and_print_response (response)
    return response['apiKey']

api_key = recover_api_key()

# phone numbers
device_ids = [11111111111, 22222222222, 33333333333, 44444444444]

test_api_helper.print_all_devices(LOCAL) # should be empty

def register_first_three_devices ():
    print ('\nDEVICE REGISTRATION:')
    for i in range(3):
        response = requests.post(url=devices_url, json={ 'device_id': device_ids[i] }, headers=build_headers(api_key)).json()
        # { "message": "Success! Device Registered." }
        assert_and_print_response (response)
    
register_first_three_devices()
test_api_helper.print_all_devices(LOCAL)

def check_device_registration (expectation, device_id):
    print ('\nCHECK IF DEVICE REGISTERED ({}):'.format(expectation))
    response = requests.get(url=devices_url, json={ 'device_id': device_id }, headers=build_headers(api_key)).json()
    # { registered: boolean whetehr or not registered }
    assert_and_print_response (response)
    
check_device_registration ('TRUE', device_ids[0])
check_device_registration ('FALSE', device_ids[3])

print_all_events()

def post_data_row (body):
    response = requests.post(url=events_url, json=body, headers=build_headers(api_key)).json()
    # { event_id: the event id generated for the POSTed row }
    assert_and_print_response (response)

print ('\nPOSTING GPS:')
# post GPS location data for user 1
post_data_row({
    'device_id': device_ids[0],                 # the associated user_id for the event_id
    'row_type': 0,                              # 0 = GPS data
    'latitude': random.uniform(-90.0, 90.0),    # -90 to 90 float range
    'longitude': random.uniform(-180.0, 180.0), # -180 to 180 float range
})
    
print ('\nPOSTING BLUTOOTH DATA:')
# simulate user 2 detecting user 3 via Blue tooth
post_data_row({
    'device_id': device_ids[1],                 # the associated user_id for the event_id
    'row_type': 1,                              # 1 = bluetooth data
    'contact_id': device_ids[2],                # other user detected by bluetooth
    'contact_level': random.uniform(0.0, 1.0),  # float value of the bluetooth signal strength
})

print ('\nPOSTING SURVEY DATA:')
def random_symptoms ():
    symptoms = ['cough', 'fever', 'nausea', 'fatigue', 'runny nose']
    return ", ".join(random.sample(symptoms, random.randint(1, len(symptoms))))

# simulate user 1 completing a symptoms survey
post_data_row({
    'device_id': device_ids[0],                 # the associated user_id for the event_id
    'row_type': 2,                              # 2 = survey data
    'symptoms': random_symptoms(),              # comma seperated string of symptoms
    'infection_status': random.randint(0, 3),   # integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered]
})

print_all_events()

def user_opt_out ():
    print ('\nUSER OPT OUT:')
    # simualte user 3 opting out of program, delete user 
    response = requests.delete(url=devices_url, json={ 'device_id': device_ids[2] }, headers=build_headers(api_key)).json()
    # { "message": "Success! Device Unregistered." }
    assert_and_print_response (response)    
    test_api_helper.print_all_devices(LOCAL)

user_opt_out()

print ('\nCHECK FOR BLUTOOTH DATA DELETE:')
# (should delete blue tooth contact row since it contains data from user 3 who just opted out)
print_all_events()

def delete_user_account ():
    print ('\nDELETE USER ACCOUNT:')
    body = { 
        'email': dev_email,
        'password': dev_password,
    }
    response = requests.delete(url=users_url, json=body, headers=build_headers()).json()
    # { "message": "User Account Deleted: some_dev2@site.com" }
    assert_and_print_response (response)

print ('\nALL TABLES:')
test_api_helper.print_all_users(LOCAL)
test_api_helper.print_all_devices(LOCAL)
print_all_events()
