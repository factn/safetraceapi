###### Testing a temporary mock database via google docs spreadsheet

url: https://safetraceapi.herokuapp.com/mockData

GET
⋅⋅⋅request body can be formatted in one of two ways:
```yaml
{
    "rows": [0, 3, 5, 2],   # rows can be an array of integer values
    "rangesFormat": false   # rows is not in ranges format
}
```
⋅⋅⋅or:
```yaml
{
    "rows": ["0-3", "5", "7-10"],   # rows can be an array of string ranges
    "rangesFormat": true   # rows is in ranges format
}
```

POST
```yaml
{
    # values is an array of rows to be appended to the end of the line
    "values": [
        [ "John", "Liverpool", 32 ],
        [ "Paul", "Queens", 23 ],
        [ "George", "Boston", 55 ],
        [ "Ringo", "Los Angeles", 27 ]
    ]
}
```

PATCH
```yaml
{
    # an array of objects containing the range to update, 
    # and an array of the new row data for that range
    "inputs": [
        {
            "range": "0-2",
            "values": [
                [ "John", "Liverpool", 32 ],
                [ "Paul", "Queens", 23 ],
                [ "George", "Boston", 55 ],
            ]
        }, 
        {
            "range": "3", # range can be a single number
            "values": [
                [ "Ringo", "Los Angeles", 27 ]
            ]
        }
    ]
}
```

DELETE
⋅⋅⋅same as the GET request body
