// TODO: options returns all columns in mini doc...

const router = require('express').Router();

const { pool } = require('./postgresql');
const queryUtils = require('./queryUtils');

const eventsTable = 'events';
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
router.get('/', queryUtils.getRequestCallback(eventsTable));

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

OUTPUT
{
    'event_id': event_id integer created for the row
}
*/

// adds single qoutes around string arguments for sql queries
function stringifyArg(arg) {
    return typeof arg === 'string' ? `'${arg}'` : arg;
}
// handle post requests
router.post('/', async (request, response, next) => {
    try {
        let keys = Object.keys(request.body);
        let values = keys.map(k=>stringifyArg(request.body[k])).join(',');       
        let sql = `INSERT INTO ${eventsTable} (${keys.join(", ")}) VALUES (${values}) RETURNING ${eventIDColumn};`;
        const queryResult = await pool.query(sql);
        response.status(201).json( queryResult.rows[0] );
    }
    catch (e) { next(e); }
});
  
module.exports = router;