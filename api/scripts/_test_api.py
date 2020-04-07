'''
    script to test the api endpoints
'''
import _clients
import _events
import _devices
import _permissions
import _test_script_utils
import _test_api_utils
import random

LOCAL = True
_permissions.BASE_URL = _clients.BASE_URL = _events.BASE_URL = _devices.BASE_URL = 'http://localhost:3000' if LOCAL else 'https://safetraceapi.herokuapp.com'

'''CLEAR THE DATABASE '''
_test_script_utils.clear_database(LOCAL)

'''REGISTER SOME CLIENTS'''
all_clients = _clients.register_test_clients()
_test_script_utils.print_all_clients(LOCAL)

'''CLIENT UPDATES ACCOUNT CREDENTIALS'''
all_clients[1] = _clients.update_client_credentials(all_clients[1])
_test_script_utils.print_all_clients(LOCAL)

'''CLIENT LOSES AND RECOVERS KEYS'''
all_clients[1] = _clients.client_lose_and_recover_keys (all_clients[1])
api_key = all_clients[1]['api_key']

'''REGISTER DEVICES'''
device_ids = [11111111111, 22222222222, 33333333333, 44444444444]
print ('\nDEVICE REGISTRATION:')    
device_keys = [ _devices.register_device (api_key, device_ids[i], i == 0) for i in range(3) ]

_test_script_utils.print_all_devices(LOCAL)

def check_device_registration (device_id, expect):
    print ('CHECK IF DEVICE REGISTERED (E: {} / V: {}):'.format(expect, _devices.check_device_registration (api_key, device_id)))
    
check_device_registration (device_ids[0], 'TRUE ')
check_device_registration (device_ids[3], 'FALSE')

'''POST SOME DATA'''
def print_events ():
    _events.print_all_events_for_clients(all_clients)

print ('\nPOSTING GPS:')
# post GPS location data for device 1
_events.post_data_row(api_key, device_keys[0], {
    'device_id': device_ids[0],                 # the associated device_id for the event
    'row_type': 0,                              # 0 = GPS data
    'latitude': random.uniform(-90.0, 90.0),    # -90 to 90 float range
    'longitude': random.uniform(-180.0, 180.0), # -180 to 180 float range
}, True)
    
print ('\nPOSTING BLUTOOTH DATA:')
# simulate device 2 detecting device 3 via Blue tooth
_events.post_data_row(api_key, device_keys[1], {
    'device_id': device_ids[1],                 # the associated device_id for the event
    'row_type': 1,                              # 1 = bluetooth data
    'contact_id': device_ids[2],                # other device detected by bluetooth
    'contact_level': random.uniform(0.0, 1.0),  # float value of the bluetooth signal strength
}, False)

def random_symptoms ():
    return ", ".join(random.sample(['cough', 'fever', 'nausea', 'fatigue', 'runny nose'], random.randint(1, 5)))
print ('POSTING SURVEY DATA:')
# simulate device 1 completing a symptoms survey
_events.post_data_row(api_key, device_keys[0], {
    'device_id': device_ids[0],                 # the associated device_id for the event
    'row_type': 2,                              # 2 = survey data
    'symptoms': random_symptoms(),              # comma seperated string of symptoms
    'infection_status': random.randint(0, 3),   # integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered]
}, False)

print_events()

'''UNREGISTER DEVICE 3'''
_devices.device_opt_out (api_key, device_ids[2])
_test_script_utils.print_all_devices(LOCAL)

print ('CHECK FOR BLUTOOTH DATA DELETE:')
# (should delete blue tooth contact row since it contains data from device 3 who just opted out)
print_events()

'''ADJUST PERMISSIONS'''
client = _permissions.get_all_clients_for_permissions(api_key)[0]

# device 2 grant permissions to client 2 since it's "a super trustworthy client"
_permissions.grant_permission (api_key, device_ids[0], client['client_id'], device_keys[0], '\nDEVICE 2 GRANTS PERMISSIONS TO CLIENT 2:')
print_events()

# device 2 no longer wants client 2 to have access to it's data
_permissions.deny_permissions (api_key, device_ids[0], client['client_id'], '\nDEVICE 2 DENIES PERMISSIONS FROM CLIENT 2:')
print_events()
  
'''DELETE CLIENT ACCOUNT'''
all_clients[1] = _clients.delete_client_account(all_clients[1])

'''SHOW ALL TABLES'''
print ('\nALL TABLES:')
_test_script_utils.print_all_clients(LOCAL)
_test_script_utils.print_all_devices(LOCAL)
_test_script_utils.print_all_permissions(LOCAL)
print_events()

'''CLEAR DATABASE'''
_test_script_utils.clear_database(LOCAL)
