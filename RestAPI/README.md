&#x1F534;
>**Disclaimer:** While we here at SafetraceAPI are committed to implementing encryption for data storage and retrieval, and MPC for secure computations, the iteration of the API outlined below is **NOT** encrypted, and will be used for testing data acquisition and visualization, while it is still a public and open source API, we suggest not storing any real life data yet!

&#x1F534;

# API Docs
>#
>**Note:** Any calls to the API that don't succeed will return an error response:
>```yaml
>{ 
>    "error": "<error message>" 
>}
>```
>#
<hr>

**Table Of Contents:**
- **[Client Accounts](#client-accounts)**
    * [Get An API Key](#create-account)
    * [Recovering Your API Key](#recover-key)
    * [Updating Account Credentials](#update-account)
    * [Deleting Your Account](#delete-account)
- **[Devices](#devices)**
    * [Registering A Device](#register-device)
    * [Unregistering A Device](#unregister-device)
    * [Checking If A Device Is Registered](#check-device)
- **[Events](#events)**
    * [Supplying Event Data](#supply-data)
    * [Getting Event Data](#get-data)
<hr>

<a name="client-accounts"></a>
# Client Accounts

**ENDPOINT URL** : `https://safetraceapi.herokuapp.com/users`
<hr>

<a name="create-account"></a>
## Get An API Key:
In order to use any API endpoints, you must register for a Safetrace account and get an API key.

**Method** : `POST`

***Request Body:***
```yaml
{
    'email': '<email>',
    'password': '<password>'
}
```
***Response:***
```yaml
{
    message: "Account Created For: <your-email>, save the API Key included in this object",
    apiKey: "<API-key>"
}
```
***Usage:***

    $ curl -X POST https://safetraceapi.herokuapp.com/users \
    -d '{ \
        "email": "<email>", \
        "password": "<password>" \
    }' \
<hr>

<a name="recover-key"></a>
## Recovering Your API Key:
**Method** : `GET`

***Request Body:***
```yaml
{
    'email': '<email>',
    'password': '<password>'
}
```
***Response:***
```yaml
{
    apiKey: "<API-key>"
}
```
***Usage:***

    $ curl -X GET https://safetraceapi.herokuapp.com/users \
    -d '{ \
        "email": "<email>", \
        "password": "<password>" \
    }' \
<hr>

<a name="update-account"></a>
## Updating Your Credentials:
**Method** : `PATCH`

***Request Body:***
```yaml
{
    'email': <email>,
    'password': '<password>',
    'newEmail': '<new-email>',          # (OPTIONAL)
    'newPassword': '<new-password>',    # (OPTIONAL)
}
```
>- You must supply either a `newEmail` or `newPassword`

***Response:***
```yaml
{
    message: "Account Credentials Updated For: <new-email>"
}
```
***Usage:***

    $ curl -X PATCH https://safetraceapi.herokuapp.com/users \
    -d '{ \
        "email": "<email>", \
        "password": "<password>", \
        "newEmail": "<new-email>", \
        "newPassword": "<new-password>" \
    }' \
<hr>

<a name="delete-account"></a>
## Deleting Your Account:
**Method** : `DELETE`

***Request Body:***
```yaml
{
    'email': '<email>',
    'password': '<password>'
}
```
***Response:***
```yaml
{
    message: "User Account Deleted: <email>"
}
```
***Usage:***

    $ curl -X DELETE https://safetraceapi.herokuapp.com/users \
    -d '{ \
        "email": "<email>", \
        "password": "<password>" \
    }' \
<hr>

<a name="devices"></a>
# Devices

**ENDPOINT URL** : `https://safetraceapi.herokuapp.com/api/devices`
<hr>

<a name="register-device"></a>
## Registering A Device:
When a Resource Owner gives consent to be registered and supply Safetrace with location and survey data, their device must be registered with a unique ID.

**Method** : `POST`

***Request Body:***
```yaml
{
    'device_id': '<phone-number>'
}
```
***Response:***
```yaml
{ 
    message: 'Success! Device Registered.' 
}
```
<hr>

<a name="unregister-device"></a>
## Unregistering A Device:
When a Resource Owner gives revokes consent to supply Safetrace with location and survey data, their device must be unregistered.
>When a device is unregistered, all rows in the Events Table that have any data concerning that device are deleted.

**Method** : `DELETE`

***Request Body:***
```yaml
{
    'device_id': '<phone-number>'
}
```
***Response:***
```yaml
{ 
    message: 'Success! Device Unregistered.' 
}
```
<hr>

<a name="check-device"></a>
## Checking If A Device Is Registered:

**Method** : `GET`

***Request Body:***
```yaml
{
    'device_id': '<phone-number>'
}
```
***Response:***
```yaml
{ 
    registered: <boolean-value> 
}
```
<hr>

<a name="events"></a>
# Events
**ENDPOINT URL** : `https://safetraceapi.herokuapp.com/api/events`

**COLUMNS:**
- `event_id` (INT)
- `time` (TIMESTAMP)
- `device_id` (INT)
- `row_type` (INT)
- `longitude` (FLOAT)
- `latitude` (FLOAT)
- `contact_id` (INT)
- `contact_level` (FLOAT)
- `symptoms` (STRING)
- `infection_status` (INT)
<hr>

<a name="supply-data"></a>
## Supplying Event Data:

**Method** : `POST`
>Attempts to `POST` data to the Events endpoints with a `device_id` that is not registered in the database will be rejected.

>Every `POST` request body must include a `row_type` key, with an integer corresponding to the types of data that an be posted where:
>- *0 = GPS Data*
>- *1 = BlueTooth Data*
>- *2 = Survey Data*

***[GPS Data] Request Body:***
```yaml
{
    "device_id": 0,       
    "row_type": 0,      
    "latitude": 45,     # -90 to 90 float range
    "longitude": 155,   # -180 to 180 float range
}
```
***[BlueTooth Data] Request Body:***
>The `contact_id` key must be a user ID found in the Users Table.  If it matches the `user_id` key, an error will be thrown.
```yaml
{
    "device_id": 0,           
    "row_type": 1,          
    "contact_id": 1,        # other user detected 
    "contact_level": .5,    # float value of the bluetooth signal strength
}
```
***[Survey Data] Request Body:***
>The `infection_status` key is an integer in the range 0 - 3 describing the test status of the user where:
>- *0 = User doesn't want to specify*
>- *1 = User doesn't know*
>- *2 = User is infected*
>- *3 = User is recovered*
```yaml
{
    "device_id": 0, 
    "row_type": 2,
    "symptoms": "cough, fever", # comma seperated string of symptoms
    "infection_status": 1,
}
```
***Response:***
```yaml
{
    "event_id": 0   # event_id integer created for the row
}
```
<hr>

<a name="get-data"></a>
## Getting Event Data:

**Method** : `GET`

***Request Body (**OPTIONAL**):***
```yaml
{
    "columns": "event_id, device_id", # (OPTIONAL) comma seperated column names
    "query": "row_type = 0"         # (OPTIONAL) an SQL query
}
```
>- if `columns` is ommited, all columns are returned per row
>- if `query` is ommited, all rows are returned

***Response:***
```yaml
{
    # rows: an array of rows that met the query criteria
    # each element contains an object corresponding to the columns specified in the request body
    "rows": [ 
        { 
            "event_id": 1, 
            "device_id": 3 
        },
        { 
            "event_id": 2, 
            "device_id": 5 
        },
    ]
}
```
#
