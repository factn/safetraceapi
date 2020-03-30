const { pool } = require('./postgresql');
const queryUtils = require('./queryUtils');

const TABLE = 'devices';
const DEVICEID = 'device_id';

/*
INPUT:
{
    'device_id': 15553332222 // phone number with country code
}
OUTPUT
{
    registered: true [or false]
}
*/
module.exports.is_device_registered = async (req, resp, next) => {
    try {
        queryUtils.assertBodyKey (DEVICEID, req.body, 'QUERY DEVICE REGISTRATION');
        const result = await pool.query(`SELECT * FROM ${TABLE} WHERE ${DEVICEID} = '${req.body[DEVICEID]}';`);
        resp.status(200).json( { registered: result.rows.length > 0 } );
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    'device_id': 15553332222 // phone number with country code
}
OUTPUT
{
    success message...
}
*/
module.exports.register_device = async (req, resp, next) => {
    try {
        queryUtils.assertBodyKey (DEVICEID, req.body, 'REGISTER DEVICE');
        const r = await pool.query(`INSERT INTO ${TABLE} (${DEVICEID}) VALUES ('${req.body[DEVICEID]}');`);
        resp.status(201).json( { message: 'Success! Device Registered.' } );
    }
    catch (e) { next(e); }
};

/*
INPUT
{
    'device_id': 034234242
}
OUTPUT device row deleted
{
    success message...
}
*/
module.exports.unregister_device = async (req, resp, next) => {
    try {
        queryUtils.assertBodyKey (DEVICEID, req.body, 'UNREGISTER DEVICE');
        const r = await pool.query(`DELETE FROM ${TABLE} WHERE ${DEVICEID} = '${req.body[DEVICEID]}';`);
        resp.status(200).json( { message: 'Success! Device Unregistered.' } );
    }
    catch (e) { next(e); }
};