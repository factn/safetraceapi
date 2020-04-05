const consts = require('./constants');
const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');
const DevicesController = require('./devices');
const a_Encryption = require('../encryption/asymmetric');


function assertClientID (req, action) {
    let clientID = assertBodyKey (req, consts.CLIENT_ID, action);
    if (clientID === consts.SAFETRACE_CLIENT_ID)
        throw new Error ('Client ID must be > 1!');
    return clientID;
}

async function asssertClientIDAndDeviceID (req, action) {
    let clientID = assertClientID (req, action);
    let deviceIDHash = await DevicesController.assertAndHashDeviceID (req, action);
    return { clientID, deviceIDHash };
}


/*
INPUT:
{
    device_id:  < device-id >,
    client_id:  < client-id >,
}
OUTPUT
{
    has_permissions: < boolean >
}
*/
module.exports.get_permissions = async (req, resp, next) => {
    try {
        let { clientID, deviceIDHash } = await asssertClientIDAndDeviceID (req, 'GET PERMISSIONS');
        const result = await db.query(`SELECT * FROM ${consts.PERMISSIONS_TABLE} WHERE ${consts.DEVICE_ID} = '${deviceIDHash}' AND ${consts.CLIENT_ID} = '${clientID}';`);
        resp.status(200).json( { has_permissions: result.rows.length > 0 } );
    }
    catch (e) { next(e); }
};


module.exports._grant_permissions = async (deviceHash, deviceKey, clientPublicKey, clientID) => {
    // encrypt the device key so that the end party can decrypt it when they need it
    let encryptedDeviceKey = a_Encryption.encryptData(deviceKey, clientPublicKey);
    await db.query(`INSERT INTO ${consts.PERMISSIONS_TABLE} (${consts.DEVICE_ID}, ${consts.CLIENT_ID}, ${consts.DEVICE_KEY}) VALUES ('${deviceHash}', '${clientID}', '${encryptedDeviceKey}');`);
};

/*
INPUT:
{
    HEADER 
    {
        device_key: < device-private-key >
    }
    device_id:  < device-id >,
    client_id:  < client-id >,
}
OUTPUT
{
    message: < confirmation message >
}
*/
module.exports.grant_permissions = async (req, resp, next) => {
    try {
        let action = 'GRANT PERMISSIONS';
        let clientID = assertClientID (req, action);
        let { deviceIDHash, deviceKey } = await DevicesController.assertDeviceIDAndKey (req, action);
        
        // get the public key of the client_id
        const result = await db.query(`SELECT ${consts.PUBLIC_KEY}, ${consts.DISPLAY_NAME} FROM ${consts.CLIENTS_TABLE} WHERE ${consts.CLIENT_ID} = ${clientID};`);
        
        if (result.rows.length <= 0)
            throw new Error(`Error! [${action}] : Client ID: '${clientID}' doesnt exist!`);
        
        let clientPublicKey = result.rows[0][consts.PUBLIC_KEY];
        
        await module.exports._grant_permissions(deviceIDHash, deviceKey, clientPublicKey, clientID);
        resp.status(200).json( { message: `Permissions Granted For ${result.rows[0][consts.DISPLAY_NAME]}` } );
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    device_id:  < device-id >,
    client_id:  < client-id >,
}
OUTPUT
{
    message: < confirmation message >
}
*/
module.exports.deny_permissions = async (req, resp, next) => {
    try {
        const action = 'DENY PERMISSIONS';
        let { clientID, deviceIDHash } = await asssertClientIDAndDeviceID (req, action);
        
        const result = await db.query(`SELECT ${consts.DISPLAY_NAME} FROM ${consts.CLIENTS_TABLE} WHERE ${consts.CLIENT_ID} = ${clientID};`);
        if (result.rows.length <= 0)
            throw new Error(`Error! [${action}] : Client ID: '${clientID}' doesnt exist!`);
                
        await db.query(`DELETE FROM ${consts.PERMISSIONS_TABLE} WHERE ${consts.DEVICE_ID} = '${deviceIDHash}' AND ${consts.CLIENT_ID} = '${clientID}';`);
        resp.status(200).json( { message: `Permissions Denied For ${result.rows[0][consts.DISPLAY_NAME]}` } );
    }
    catch (e) { next(e); }
};