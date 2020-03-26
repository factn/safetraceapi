'''
    script to test the api endpoints

    USER REGISTRATION:
    1) register a user with a phone number and receive their user_ids
    2) register user 2 and 3 with numbers
    3) retreive user 2's user id via phone number (in case it's lost or something)

    GPS POSTING
    4) post GPS location data for user 1
    
    BLUE TOOTH CONTACT
    5) simulate user 2 detecting user 3 via Blue tooth

    SURVEY
    6) simulate user 1 completing a symptoms survey

    USER OPT OUT
    7) simualte user 3 opting out of program, delete user 
        (should delete blue tooth contact row)
'''

from __future__ import print_function
import random
import requests
import json
import os

LOCAL = False


'''CLEAR THE DATABASE FOR TESTING PURPOSES'''
print ('\nCLEARING DATABASE:')
if LOCAL:
    os.system('cat RestAPI/scripts/initializeDB.sql | psql -d safetrace_api -U safetrace_user')
else:
    os.system('cat RestAPI/scripts/initializeDB.sql | heroku pg:psql')
'''END DATABASE CLEARING'''

'''HELPER FUNCTIONS'''
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

'''END HELPER FUNCTIONS'''



if LOCAL:
    url = 'http://localhost:3000'
else:
    url = 'https://safetraceapi.herokuapp.com'

url += '/api'
users_url = url + '/users'

# SHOWS HOW TO GET ALL DATA FROM A TABLE
def print_all_table (url, title):
    print ('\n{}:'.format(title))
    response = requests.get(url=url, json={}).json()
    '''
    response = {
        rows: an array of json objects containing keys for each column requested 
                (all columns if no specific columns specified)
    }
    '''
    rows = response['rows']
    for i in range(len(rows)):
        print_obj (rows[i])

def print_all_users ():
    print_all_table(users_url, 'USERS')
    
def print_all_events():
    print_all_table(url, 'EVENTS')
    
'''USER REGISTRATION:'''
# phone numbers
user_numbers = [15554443333, 19998887777, 12223334444]
user_ids = [None, None, None]

print_all_users() # should be empty

print ('\nUSER REGISTRATION:')
for i in range(3):
    user_registration_body = { 
        'phone_number': user_numbers[i] 
    }
    response = requests.post(url=users_url, json=user_registration_body).json()
    '''
    response = {
        user_id: user_id created for the user
    }
    '''
    print_obj_simple (response)
    user_ids[i] = response['user_id']

print_all_users()


print ('\nRETREIVE USER ID VIA PHONE NUMBER:')
user_ids[1] = None # 'lose' the user_id
print (user_ids)

# this request body gets the user_id column, for the row where phone_number = user's number
body = {
    "columns": "user_id",
    "query": "phone_number = {}".format(user_numbers[1])
}
response = requests.get(url=users_url, json=body).json()
'''
response = {
    rows: array of json objects
}
'''
print_obj_simple (response['rows'][0])
user_ids[1] = response['rows'][0]['user_id']
print (user_ids)

print_all_users()

print ('\nUPDATE UESR PHONE NUMBER VIA ID:')
params = {
    'user_id': user_ids[1],
    'phone_number': 1234
}
response = requests.patch(url=users_url, json=params).json()
'''
returns the updated user row
response = {
    user_id: the user's id,
    phone_number: updated number
}
'''
print_obj (response)

print_all_users()
print_all_events()

'''GPS POSTING'''
print ('\nPOSTING GPS:')
# post GPS location data for user 1
gps_body = {
    'user_id': user_ids[0],                     # the associated user_id for the event_id
    'row_type': 0,                              # 0 = GPS data
    'latitude': random.uniform(-90.0, 90.0),    # -90 to 90 float range
    'longitude': random.uniform(-180.0, 180.0), # -180 to 180 float range
}
response = requests.post(url=url, json=gps_body).json()
'''
response = {
    event_id: the event id generated for the POST
}
'''
print_obj_simple (response)

'''BLUTOOTH POSTING'''
print ('\nPOSTING BLUTOOTH DATA:')
# simulate user 2 detecting user 3 via Blue tooth
bluetooth_body = {
    'user_id': user_ids[1],                     # the associated user_id for the event_id
    'row_type': 1,                              # 1 = bluetooth data
    'contact_id': user_ids[2],                  # other user detected by bluetooth
    'contact_level': random.uniform(0.0, 1.0),  # float value of the bluetooth signal strength
}
response = requests.post(url=url, json=bluetooth_body).json()
print_obj_simple (response)

'''SURVEY POSTING'''
print ('\nPOSTING SURVEY DATA:')

def random_symptoms ():
    symptoms = ['cough', 'fever', 'nausea', 'fatigue', 'runny nose']
    return ", ".join(random.sample(symptoms, random.randint(1, len(symptoms))))

# simulate user 1 completing a symptoms survey
survey_body = {
    'user_id': user_ids[0],                     # the associated user_id for the event_id
    'row_type': 2,                              # 2 = survey data
    'symptoms': random_symptoms(),              # comma seperated string of symptoms
    'infection_status': random.randint(0, 3),   # integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered]
}

response = requests.post(url=url, json=survey_body).json()
'''
response = {
    event_id: the event id generated for the POST
}
'''

print_obj_simple (response)

print_all_events()

'''USER OPT OUT'''
print ('\nUSER OPT OUT:')
# simualte user 3 opting out of program, delete user 
    
delete_body = {
    "query": "user_id = {}".format(user_ids[2])
}
response = requests.delete(url=users_url, json=delete_body).json()
'''
response = {
    rows: array of json objects representing the users that were deleted
}
'''


print_obj (response)

print_all_users()

print ('\nCHECK FOR BLUTOOTH DATA DELETE:')
# (should delete blue tooth contact row since it contains data from user 3 who just opted out)
print_all_events()