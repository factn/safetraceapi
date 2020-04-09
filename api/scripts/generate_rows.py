'''
    script to generate dummy data on the DB
    TODO: print events to check afterwards.....
'''
import _events
import _devices
import _test_script_utils
import _test_api_utils
import random
import time 
import sys

DEVICE_COUNT = 1
ROWS_COUNT = 1

_events.BASE_URL = _devices.BASE_URL = 'https://safetraceapi.herokuapp.com'

# _test_script_utils.print_all_clients(False)
# _test_script_utils.print_all_devices(False)
# _test_script_utils.print_all_permissions(False)
# exit()




safetrace_client = _test_script_utils.create_safetrace_client()
api_key = safetrace_client['api_key']

'''REGISTER DEVICES'''
device_ids = [ str(12) * 11 for i in range(DEVICE_COUNT) ]
print ('\nDEVICE REGISTRATION:')    
device_keys = [ _devices.register_device (safetrace_client['api_key'], device_ids[i], True) for i in range(DEVICE_COUNT) ]
_test_script_utils.print_all_devices(False)

def get_gps_data (device_id):
    return {
        'device_id': device_id,                 # the associated device_id for the event
        'row_type': 0,                              # 0 = GPS data
        'latitude': random.uniform(-90.0, 90.0),    # -90 to 90 float range
        'longitude': random.uniform(-180.0, 180.0), # -180 to 180 float range
    }
def get_bt_data (device_id, contact_id):
    return {
        'device_id': device_id,                 # the associated device_id for the event
        'row_type': 1,                              # 1 = bluetooth data
        'contact_id': contact_id,                # other device detected by bluetooth
        'contact_level': random.uniform(0.0, 1.0),  # float value of the bluetooth signal strength
    }

def random_symptoms ():
    return ", ".join(random.sample(['cough', 'fever', 'nausea', 'fatigue', 'runny nose'], random.randint(1, 5)))

def get_survey_data (device_id):
    return {
        'device_id': device_id,                 # the associated device_id for the event
        'row_type': 2,                              # 2 = survey data
        'symptoms': random_symptoms(),              # comma seperated string of symptoms
        'infection_status': random.randint(0, 3),   # integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered]
    }

for i in range(ROWS_COUNT):
    time.sleep(.1)
    print ('Adding Row: ' + str(i) + "\r")
    sys.stdout.write("\033[F") # Cursor up one line

    device_idx = random.randint(0, len(device_ids) - 1)
    device_id = device_ids[device_idx]
    device_key = device_keys[device_idx]

    row_type = random.randint(0, 2)
    
    if row_type == 0:
        body = get_gps_data (device_id)
    
    elif row_type == 1:
        contact_id = device_id
        while contact_id == device_id:
            contact_id = random.choice(device_ids)

        body = get_bt_data (device_id, contact_id)

    elif row_type == 2:

        body = get_survey_data (device_id)
    
    # if i % 25 == 0:
    print ('')

    # _events.post_data_row(api_key, device_key, body, i % 25 == 0)
    _events.post_data_row(api_key, device_key, body, True)
    
print ('')        
print ('Done!\n\n')