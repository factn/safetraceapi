const consts = require('./constants');
const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');
const hashing = require('../encryption/hashing');
const s_Encryption = require('../encryption/symmetric');
const PermissionsController = require('./permissions');

const TABLE = 'devices';

// check if the device id is supplied, then hash it to check against the
// database IDs
module.exports.assertAndHashDeviceID = async (request, action) => {
    return (await hashing.hashString(String(assertBodyKey (request, consts.DEVICE_ID, action))));
};

module.exports.assertDeviceIDAndKey = async (request, action) => {
    let deviceIDHash = await module.exports.assertAndHashDeviceID (request, action);
    let deviceKey = assertHeaderKey(request, consts.DEVICE_KEY, action);
    return { deviceIDHash, deviceKey };
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
        const result = await db.query(`SELECT * FROM ${TABLE} WHERE ${consts.DEVICE_ID} = '${(deviceIDHash)}';`);
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
        await db.query(`INSERT INTO ${TABLE} (${consts.DEVICE_ID}) VALUES ('${deviceIDHash}');`);
        
        // TEMPORARY: AUTOMATICALLY GRANT PERMISSION TO SAFETRACE (FOR DEVELOPMENT PURPOSES)
        await PermissionsController._grant_permissions(deviceIDHash, deviceKey, process.env.SAFETRACE_PUBLIC_KEY, consts.SAFETRACE_CLIENT_ID);

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
    device_id: < device-id >
}
OUTPUT
{
    message: < success message >
}
*/
module.exports.unregister_device = async (request, resp, next) => {
    try {
        let deviceIDHash = await module.exports.assertAndHashDeviceID (request, 'UNREGISTER DEVICE');
    
        // delete device id from devices table 
        // ( This deletes all Events and Permissions rows that contain this ID )
        await db.query(`DELETE FROM ${TABLE} WHERE ${consts.DEVICE_ID} = '${deviceIDHash}';`);
        
        resp.status(200).json( { message: 'Success! Device Unregistered.' } );
    }
    catch (e) { next(e); }
};