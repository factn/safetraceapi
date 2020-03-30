
const queryUtils = require('./queryUtils');
const { pool } = require('./postgresql');

const TABLE = 'events';
const EVENTID = 'event_id';
const DEVICEID = 'device_id';
const ROWTYPE = 'row_type';

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

module.exports.get_events = async (req, response, next) => {
    try {
        const QUERY = 'query';
        const COLUMNS = 'columns';
        let sql = `SELECT ${req.body[COLUMNS] || '*'} FROM ${TABLE}`;
        if (QUERY in req.body)
            sql += ` WHERE ${req.body[QUERY]}`;

        const result = await pool.query(sql + ';');
        response.status(200).json( { rows: result.rows } );

    }
    catch (e) { next(e); }
};


/*
GPS DATA = 
{
    'device_id': 0,     // the associated device_id for the event
    'row_type': 0,      // integer 0 - 2 [0: GPS] [1: BlueTooth] [2: Survey]
    'latitude': 45,     // -90 to 90 float range
    'longitude': 155,   // -180 to 180 float range
}
BLUETOOTH DATA = 
{
    'device_id': 0,         // the associated device_id for the event
    'row_type': 1,          // integer 0 - 2 [0: GPS] [1: BlueTooth] [2: Survey]
    'contact_id': 1,        // other device detected by bluetooth
    'contact_level': .5,    // float value of the bluetooth signal strength
}
SURVEY DATA = 
{
    'device_id': 0,             // the associated device_id for the event
    'row_type': 2,              // integer 0 - 2 [0: GPS] [1: BlueTooth] [2: Survey]
    'symptoms': 'cough, fever', // comma seperated string of symptoms
    'infection_status': 1,      // integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered]
}
OUTPUT
{
    'event_id': event_id integer created for the row
}
*/
module.exports.post_event = async (req, response, next) => {
    try {
        let action = 'POST EVENT'
        queryUtils.assertBodyKey (DEVICEID, req.body, action);
        queryUtils.assertBodyKey (ROWTYPE, req.body, action);
        
        // adds single qoutes around string arguments for sql queries
        function stringifyArg(arg) {
            return typeof arg === 'string' ? `'${arg}'` : arg;
        }
        let keys = Object.keys(req.body);
        let values = keys.map(k => stringifyArg(req.body[k])).join(',');       
        const result = await pool.query(`INSERT INTO ${TABLE} (${keys.join(", ")}) VALUES (${values}) RETURNING ${EVENTID};`);
        response.status(201).json( result.rows[0] );
    }
    catch (e) { next(e); }
}