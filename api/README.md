&#x1F534;
>#
>**Disclaimer:** While we here at SafetraceAPI are committed to implementing MPC for secure computations, the iteration of the API outlined below is **NOT** MPC compatible, and will be used for testing data acquisition and visualization, while it is still a public and open source API, we suggest not storing any real life data yet!
>#
&#x1F534;

# API Docs

### BASE URL: `https://safetraceapi.herokuapp.com`

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
    * [Getting API Keys](#create-account)
    * [Recovering Your API Keys](#recover-key)
    * [Updating Account Credentials](#update-account)
    * [Deleting Your Account](#delete-account)
- **[Using Your API Key](#using-key)**
- **[Devices](#devices)**
    * [Registering A Device](#register-device)
    * [Unregistering A Device](#unregister-device)
    * [Checking If A Device Is Registered](#check-device)
- **[Permissions](#permissions)**
    * [Available Clients](#available-clients)
    * [Granting Permissions](#grant-permission)
    * [Denying Permissions](#deny-permission)
    * [Checking Client-Device Permissions](#check-permission)
- **[Events](#events)**
    * [Encrypting Event Data](#encrypt-data)
    * [Posting Event Data](#post-data)
    * [Getting Event Data](#get-data)
<hr>

<a name="client-accounts"></a>
# Client Accounts

<a name="create-account"></a>
## Getting API Keys:
In order to use any API endpoints, you must register for a Safetrace account and get an API key.

**Method** : `POST <base-url>/clients`

***Header:***
```yaml
{
    email:      < email >,
    password:   < password >
}
```
***Request Body:***
```yaml
{
    display_name:   < display name >,
    bio:            < a short bio >
}
```
***Response:***
```yaml
{
    message:        "Account Created For: < email >, save the API and Private Keys included in this object. Make sure to keep them private and secure",
    api_key:        < api key >,
    private_key:    < private key >,
    public_key:     < public key >
}
```
***Usage:***

    $ curl -X POST <base-url>/clients \
    -H 'email: < email >' \
    -H 'password: < password >' \
    -d '{ \
        "display_name": "< display name >", \
        "bio": "< bio >" \
    }' \
<hr>

<a name="recover-key"></a>
## Recovering Your API Keys:

**Method** : `GET <base-url>/clients/keys`

***Header:***
```yaml
{
    email:      < email >,
    password:   < password >
}
```
***Response:***
```yaml
{
    api_key:        < API-key >,
    private_key:    < private-key >,
    public_key:     < public key >
}
```
***Usage:***

    $ curl -X GET <base-url>/clients/keys \
    -H 'email: < email >' \
    -H 'password: < password >' \
<hr>

<a name="update-account"></a>
## Updating Your Credentials:

**Method** : `PATCH <base-url>/clients/`
***Header:***
```yaml
{
    email:      < email >,
    password:   < password >
}
```
***Request Body:***
```yaml
{
    new_email:      < [ OPTIONAL ] new-email >,    
    new_password:   < [ OPTIONAL ] new-password >, 
}
```
>#
>You must supply either a `newEmail` or `newPassword`
>#

***Response:***
```yaml
{
    message: "Account Credentials Updated For: <new-email>"
}
```
***Usage:***

    $ curl -X PATCH <base-url>/clients \
    -H 'email: < email >' \
    -H 'password: < password >' \
    -d '{ \
        "newEmail": "<new-email>", \
        "newPassword": "<new-password>" \
    }' \
<hr>

<a name="delete-account"></a>
## Deleting Your Account:

**Method** : `DELETE <base-url>/clients`

***Header:***
```yaml
{
    email:      < email >,
    password:   < password >
}
```
***Response:***
```yaml
{
    message:    "User Account Deleted: <email>"
}
```
***Usage:***

    $ curl -X DELETE <base-url>/clients \
    -H 'email: < email >' \
    -H 'password: < password >' \
    
<hr>

<a name="using-key"></a>
# Using Your API Key
All HTTP requests to the API must include your API key in the header, under header key: `api_key`.
    
    api_key: < your api key >
<hr>

<a name="devices"></a>
# Devices

<a name="register-device"></a>
## Registering A Device:
When a Resource Owner gives consent to be registered and supply Safetrace with location and survey data, their device must be registered with a unique ID.

**Method** : `POST <base-url>/api/devices`

***Request Body:***
```yaml
{
    device_id: < phone-number >
}
```
***Response:***
```yaml
{ 
    message:    "Success! Device Registered. Save the 'device_key' included in this object securely, it can only be supplied once!",
    device_key: < device-key >
}
```

&#x1F534;
>#
>The `device_key` returned when registering a device is not saved to the database and **MUST** be saved securely (preferrably in the device's local storage).  
>
>The key is used to verify the device for API calls, and to encrypt any data pertaining to the device.
>#
&#x1F534;

<hr>

<a name="unregister-device"></a>
## Unregistering A Device:
When a Resource Owner gives revokes consent to supply Safetrace with location and survey data, their device must be unregistered.

>#
>When a device is unregistered, all rows in the **[Events](#events)** and **[Permissions](#permissions)** Tables that have any data pertaining to that device are deleted.
>#

**Method** : `DELETE <base-url>/api/devices`

***Header:***
```yaml
{
    api_key:    < api key >,
    device_key: < device-key for the device to be unregistered >
}
```
***Request Body:***
```yaml
{
    device_id: < phone-number >
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

**Method** : `GET <base-url>/api/devices`

***Request Body:***
```yaml
{
    device_id: < phone-number >
}
```
***Response:***
```yaml
{ 
    registered: < boolean > 
}
```
<hr>


<a name="permissions"></a>
# Permissions

Every device owner will have the choice of which clients they will allow to access their data.
<hr>

<a name="available-clients"></a>
## Available Clients:

**Method** : `GET <base-url>/clients`

Gets the list of available clients to show the device owner.

***Header:***
```yaml
{
    api_key: < api key >,
}
```
***Response:***
```yaml
{
    "clients": [ 
        { 
            client_id:      < client id >, 
            display_name:   < display name >, 
            bio:            < client bio >
        }, 
        { ... },
        { ... },
    ]
}
```
<hr>

<a name="grant-permission"></a>
## Granting Permissions:

**Method** : `POST <base-url>/api/permissions`

Granting permission will allow a client with `client_id` to access the data rows with information about the device with `device_id`.

***Header:***
```yaml
{
    api_key:    < api key >,
    device_key: < device key of the device granting permissions >
}
```
***Request Body:***
```yaml
{
    device_id:  < device-id granting permissions >,
    client_id:  < client-id >,
}
```
***Response:***
```yaml
{ 
    message: "Permissions Granted For < client display name >"
}
```
<hr>

<a name="deny-permission"></a>
## Denying Permissions:
Denying permission will prohibit a client with `client_id` from accessing data rows with information about the device with `device_id`.

**Method** : `DELETE <base-url>/api/permissions`

***Header:***
```yaml
{
    api_key:    < api key >,
    device_key: < device key of the device denying permissions >
}
```
***Request Body:***
```yaml
{
    device_id:  < device-id denying permissions >,
    client_id:  < client-id >,
}
```
***Response:***
```yaml
{ 
    message: "Permissions Denied For < client display name >"
}
```
<hr>

<a name="check-permission"></a>
## Checking Client-Device Permissions:
Check if a device has given a client permission to access their data.

**Method** : `GET <base-url>/api/permissions`

***Request Body:***
```yaml
{
    device_id:  < device-id >,
    client_id:  < client-id >,
}
```
***Response:***
```yaml
{ 
    has_permissions: < boolean >
}
```
<hr>

<a name="events"></a>
# Events

**COLUMNS:**
> All **[ Hashed ]** and **[ Encrypted ]** values are stored as `string` types in the database.

Name | Type | _
--- | --- | ---
**event_id** | `int` | 
**time** | `timestamp` | 
**device_id** | `string` | **Hashed**
**row_type** | `int` | 
**longitude** | `float` | **Encrypted**
**latitude** | `float` | **Encrypted**
**contact_id** | `int` | **Hashed**
**contact_level** | `float` | **Encrypted**
**symptoms** | `string` | **Encrypted**
**infection_status** | `int` | **Encrypted**

<hr>

<a name="encrypt-data"></a>
## Encrypting Event Data:
As a temporary endpoint before true end to end encryption is implemented, you must post the unencrypted event data to be encrypted and returned here, before posting it to the database.

**Method** : `POST <base-url>/api/encryption`

***Header:***
```yaml
{
    api_key:    < api key >,
    device_key: < device key for the device the data pertains to >
}
```

>#
>Every event data body must include a `row_type` key, with an integer corresponding to the types of data that an be posted where:
>- `0 = GPS Data`
>- `1 = BlueTooth Data`
>- `2 = Survey Data`
>#

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
>#
>The `contact_id` key must be a registered Device ID.  If it matches the `device_id` key, an error will be thrown.
>#
```yaml
{
    "device_id": 0,           
    "row_type": 1,          
    "contact_id": 1,        # other device detected 
    "contact_level": .5,    # float value of the bluetooth signal strength
}
```
***[Survey Data] Request Body:***
>#
>The `infection_status` key is an integer in the range 0 - 3 describing the test status of the Resource Owner where:
>- `0 = Resource Owner doesn't want to specify`
>- `1 = Resource Owner doesn't know`
>- `2 = Resource Owner is infected`
>- `3 = Resource Owner is recovered`
>#
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
    encrypted_body: < an object with all the proper keys encrypted and ready to send to the event data table >
}
```
<hr>

<a name="post-data"></a>
## Posting Event Data:

**Method** : `POST <base-url>/api/events`
>#
>Attempts to `POST` data to the Events endpoints with a `device_id` that is not registered in the database will be rejected.
>#

***Header:***
```yaml
{
    api_key:    < api key >,
    device_key: < device key for the device the data pertains to >
}
```
***Request Body:***

&#x1F534; The request body for posting a data row to the database **MUST** be encrypted. &#x1F534;

Use the returned `encrypted_body` value from the encryption API endpoint. See [Encrypting Event Data](#encrypt-data).

***Response:***
```yaml
{
    event_id: < event_id integer created for the row >
}
```
<hr>

<a name="get-data"></a>
## Getting Event Data:

>#
>**You will only receive rows that you have access to based on the permissions given by device owners !**
>#
**Method** : `GET <base-url>/api/events`

***Header:***
```yaml
{
    api_key:        < api key >,
    private_key:    < your client private key >
}
```
***Request Body:***
```yaml
{
    public_key: < your client public key >,
    columns:    < [ OPTIONAL ] comma seperated column names >,
    query:      < [ OPTIONAL ] an SQL query >
}
```
>#
>- if `query` is ommited, all rows are returned
>- if `columns` is ommited, all columns are returned per row
>#

***Response:***
```yaml
{
    rows: [ 
        { 
            < object representing the row with all the columns that were requested >
        },
        { ... },
        { ... },
    ]
}
```
#
