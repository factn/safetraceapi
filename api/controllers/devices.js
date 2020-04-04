const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');

const hashing = require('../encryption/hashing');
const bcrypt = require('bcrypt');

const s_Encryption = require('../encryption/symmetric');

const PermissionsController = require('./permissions');

const TABLE = 'devices';
const DEVICE_ID = 'device_id';
const DEVICE_KEY = 'device_key';

const SAFETRACE_CLIENT_ID = 1;

// check if the device id is supplied, then hash it to check against the
// database IDs
module.exports.assertAndHashDeviceID = async (request, action) => {
    return (await hashing.hashString(String(assertBodyKey (request, DEVICE_ID, action))));
};

async function getDeviceByID (deviceIDHash) {
    const result = await db.query(`SELECT * FROM ${TABLE} WHERE ${DEVICE_ID} = '${deviceIDHash}';`);
    return result.rows.length > 0 ? result.rows[0] : null;
}

async function _assertDeviceAuth (deviceIDHash, request, action) {
    let deviceKey = assertHeaderKey(request, DEVICE_KEY, action);
    function throwAuthError () {
        throw new Error(`${action} :: Device Authorization Failed [Invalid Device ID Or Device Key]!`);
    }
    let device = await getDeviceByID(deviceIDHash);
    if (!device) 
        throwAuthError ();
    if (!(await bcrypt.compare(deviceKey, device[DEVICE_KEY])))
        throwAuthError ();
    return { deviceIDHash, deviceKey };
}

module.exports.assertDeviceAuth = async (request, action) => {
    let deviceIDHash = await module.exports.assertAndHashDeviceID (request, action);
    return (await _assertDeviceAuth (deviceIDHash, request, action));
}

module.exports.assertDeviceAuthHashed = async (request, action) => {
    return (await _assertDeviceAuth (assertBodyKey (request, DEVICE_ID, action), request, action));
}

/*
INPUT:
{
    device_id: < device-id >
}
OUTPUT
{
    registered: < boolean >
}
*/
module.exports.is_device_registered = async (request, resp, next) => {
    try {
        let deviceIDHash = await module.exports.assertAndHashDeviceID (request, 'QUERY DEVICE REGISTRATION');

        console.log(deviceIDHash);
        const result = await db.query(`SELECT * FROM ${TABLE} WHERE ${DEVICE_ID} = '${(deviceIDHash)}';`);

        resp.status(200).json( { registered: result.rows.length > 0 } );
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    device_id: < device-id >
}
OUTPUT
{
    message:    "Success! Device Registered. Save the "device_key" included in this object securely, it can only be supplied once!"",
    device_key: < device-key >
}
*/
module.exports.register_device = async (request, resp, next) => {
    try {
        let deviceIDHash = await module.exports.assertAndHashDeviceID (request, 'REGISTER DEVICE');
        // generate a unique key for the device, to encrypt data
        const deviceKey = s_Encryption.getKey();

        // add the device to the devices table
        await db.query(`INSERT INTO ${TABLE} (${DEVICE_ID}, ${DEVICE_KEY}) VALUES ('${deviceIDHash}', '${(await hashing.hashStringRandom(deviceKey))}');`);
        
        // TEMPORARY: AUTOMATICALLY GRANT PERMISSION TO SAFETRACE (FOR DEVELOPMENT PURPOSES)
        await PermissionsController._grant_permissions(deviceIDHash, deviceKey, process.env.SAFETRACE_PUBLIC_KEY, SAFETRACE_CLIENT_ID);

        resp.status(201).json( { 
            message: 'Success! Device Registered. Save the "device_key" included in this object securely, it can only be supplied once!',
            device_key: deviceKey
        } );
    }
    catch (e) { next(e); }
};

/*
INPUT
{
    HEADER 
    {
        device_key: < device-private-key >
    }
    device_id: < device-id >
}
OUTPUT
{
    message: < success message >
}
*/
module.exports.unregister_device = async (request, resp, next) => {
    try {
        // make sure the device ID and device key match up
        let { deviceIDHash, deviceKey } = await module.exports.assertDeviceAuth (request, 'UNREGISTER DEVICE');
        
        // delete device id from devices table 
        // ( This deletes all Events and Permissions rows that contain this ID )
        await db.query(`DELETE FROM ${TABLE} WHERE ${DEVICE_ID} = '${deviceIDHash}';`);
        
        resp.status(200).json( { message: 'Success! Device Unregistered.' } );
    }
    catch (e) { next(e); }
};