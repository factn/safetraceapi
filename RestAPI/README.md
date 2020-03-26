&#x1F534;
>**Disclaimer:** While we here at SafetraceAPI are committed to implementing encryption for data storage and retrieval, and MPC for secure computations, the iteration of the API outlined below is **NOT** encrypted, and will be used for testing data acquisition and visualization, while it is still a public and open source API, we suggest not storing any real life data yet!

&#x1F534;

# API Docs
**Root URL** `https://safetraceapi.herokuapp.com/api`
>#
>Any Calls to the API that don't succeed will return an error response:
>```yaml
>{ 
>    "error": "[Error Message]" 
>}
>```
>#

>#
>Any Calls to the Events API (posting data to the >Events Table) require an associated `user_id` that >corresponds to a user in the Users Table.
>#

# Users Table
**URL** : `/users`

**COLUMNS:**
- `user_id` (INT)
- `phone_number` (INT)
#
**Method** : `GET`

***Request Body (**OPTIONAL**):***
```yaml
{
    "columns": "user_id, phone_number", # (OPTIONAL) comma seperated column names
    "query": "user_id = 0"              # (OPTIONAL) an SQL query
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
            "user_id": 1, 
            "phone_number": 5555555555 
        },
        { 
            "user_id": 2, 
            "phone_number": 7777777777 
        },
    ]
}
```
#
**Method** : `POST`

***Request Body:***
```yaml
{
    # phone number as integer with country code
    "phone_number": 15553332222 
}
```
***Response:***
```yaml
{
    # user_id integer created for user with phone number
    "user_id": 0 
}
```
#
**Method** : `PATCH`

***Request Body:***
```yaml
{
    "user_id": 0,               # the user id to update
    "phone_number": 15553332222 # phone number with country code to update
}
```
***Response:***
```yaml
# the complete updated row
{
    "user_id": 0,
    "phone_number": 15553332222
}
```
#
**Method** : `DELETE`

***Request Body:***
```yaml
{
    "user_id": 0 # user id to delete
}
```
***Response:***
```yaml
# user row deleted
{
    "user_id": 0,               
    "phone_number": 15553332222 
}
```
#
# Events Table
**URL** : `/events`

**COLUMNS:**
- `event_id` (INT)
- `time` (TIMESTAMP)
- `user_id` (INT)
- `row_type` (INT)
- `longitude` (FLOAT)
- `latitude` (FLOAT)
- `contact_id` (INT)
- `contact_level` NUMERIC,
- `symptoms` (STRING)
- `infection_status` (INT)
#
**Method** : `GET`

***Request Body (**OPTIONAL**):***
```yaml
{
    "columns": "event_id, user_id", # (OPTIONAL) comma seperated column names
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
            "user_id": 3 
        },
        { 
            "event_id": 2, 
            "user_id": 5 
        },
    ]
}
```
#
**Method** : `POST`
>Every `POST` request body must include a `user_id` key, with a valid user id found in the Users Table.

>Every `POST` request body must include a `row_type` key, with an integer corresponding to the types of data that an be posted where:
>- *0 = GPS Data*
>- *1 = BlueTooth Data*
>- *2 = Survey Data*

***[GPS Data] Request Body:***
```yaml
{
    "user_id": 0,       
    "row_type": 0,      
    "latitude": 45,     # -90 to 90 float range
    "longitude": 155,   # -180 to 180 float range
}
```
***[BlueTooth Data] Request Body:***
>The `contact_id` key must be a user ID found in the Users Table.  If it matches the `user_id` key, an error will be thrown.
```yaml
{
    "user_id": 0,           
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
    "user_id": 0, 
    "row_type": 2,
    "symptoms": "cough, fever", # comma seperated string of symptoms
    "infection_status": 1,
}
```
***Response:***
```yaml
# event_id integer created for the row
{
    "event_id": 0 
}
```
#
