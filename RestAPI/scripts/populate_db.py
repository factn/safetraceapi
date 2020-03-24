'''
Script to populate the test database with randomized values
'''
import random
import requests
import json

url = 'https://safetraceapi.herokuapp.com/testDB'
# url = 'http://localhost:3000/testDB'

encryption = 'mpc'
location_type = 'gps'
all_symptoms = ['cough', 'fever', 'nausea', 'fatigue', 'runny nose']

def get_random_location ():
    return 'lat:{}|lon:{}'.format(random.uniform(-90.0, 90.0), random.uniform(-180.0, 180.0))

def get_random_symptoms ():
    return ", ".join(random.sample(all_symptoms, random.randint(0, len(all_symptoms))))

def get_random_user_id ():
    return str(random.randint(0, 100))

# returns a random time string in the format 'hh:mm:ss'
def get_random_time ():
    def rand (mx):
        return str(random.randint(0, mx)).zfill(2)
    return '{}:{}:{}'.format(rand(23), rand(59), rand(59))

def build_random_datapoint ():
    return {
        'user_id': get_random_user_id(),
        'encryption': encryption,
        'time': get_random_time(),
        'location_type': location_type,
        'location': get_random_location(),
        'symptoms': get_random_symptoms()
    }


post_amount = 10

post_data = {
  'values': [build_random_datapoint() for i in range(post_amount)]
}

print 'Posting Data:'
# print post_data

# sending post request and saving response as response object 
response = requests.post(url = url, json = post_data) 

print 'Response:'
print json.dumps(response.json())

print '\n\nGetting Data:'

# event_id
# allColumns = ['user_id', 'encryption', 'time', 'location_type', 'location', 'symptoms']

params = {
    "columns": "event_id, user_id",
    "query": "user_id < 5"
}

response = requests.get(url = url, params = params) 
  
print 'Response:'
print json.dumps(response.json())