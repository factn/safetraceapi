// TODO: options returns all columns in mini doc...

const router = require('express').Router();

const { pool } = require('./postgresql');
const queryUtils = require('./queryUtils');

const mainTable = 'main_table';
const eventIDColumn = 'event_id';

/*
INPUT:
{
    'columns': 'event_id, time' // comma seperated column names (optional, default is all)
    'query': 'event_id = 0'     // an SQL query (optional)
}
OUTPUT: array of rows returned
{
    rows: [ 
        { event_id: x, time: xxxxxx, ... }, 
        { event_id: y, time: yyyyyy, ... }, 
        ...
    ]
}

*/
// handle get requests
router.get('/', queryUtils.getRequestCallback(mainTable));

/*
GPS DATA
body = {
    'user_id': 0,       // the associated user_id for the event_id
    'row_type': 0,      // integer 0 - 3 [0: GPS] [1: BlueTooth] [2: Survey] [3: QR scan]
    'latitude': 45,     // -90 to 90 float range
    'longitude': 155,   // -180 to 180 float range
}

BLUETOOTH DATA
body = {
    'user_id': 0,           // the associated user_id for the event_id
    'row_type': 1,          // integer 0 - 3 [0: GPS] [1: BlueTooth] [2: Survey] [3: QR scan]
    'contact_id': 1,        // other user detected by bluetooth
    'contact_level': .5,    // float value of the bluetooth signal strength
}

SURVEY DATA
body = {
    'user_id': 0,               // the associated user_id for the event_id
    'row_type': 2,              // integer 0 - 3 [0: GPS] [1: BlueTooth] [2: Survey] [3: QR scan]
    'symptoms': 'cough, fever', // comma seperated string of symptoms
    'infection_status': 1,      // integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered]
}

QR SCAN DATA
body = {
    'user_id': 0,               // the associated user_id for the event_id
    'row_type': 3,              // integer 0 - 3 [0: GPS] [1: BlueTooth] [2: Survey] [3: QR scan]
    'qr_data': '234dsssg',      // qr scan data as string
}


OUTPUT
{
    'event_id': event_id integer created for the row
}

*/

// handle post requests
router.post('/', async (request, response, next) => {
    try {
        let keys = Object.keys(request.body);
        let values = keys.map(k=>queryUtils.stringifyArg(request.body[k])).join(',');       
        let sql = `INSERT INTO ${mainTable} (${keys.join(", ")}) VALUES (${values}) RETURNING ${eventIDColumn};`;
        // response.status(201).json( { sql: sql } );
        const queryResult = await pool.query(sql);
        response.status(201).json( queryResult.rows[0] );
    }
    catch (e) { next(e); }
});
    
/*
INPUT 
{
    'query': 'event_id = 0' // an SQL query
}
OUTPUT array of rows deleted
{
    rows: [ 
        { event_id: x, time: xxxxxx, ... }, 
        { event_id: y, time: yyyyyy, ... }, 
        ...
    ]
}
*/
// handle delete requests
// router.delete ('/', queryUtils.deleteRequestCallback(mainTable));

module.exports = router;