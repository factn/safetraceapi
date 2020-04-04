const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');

const DevicesController = require('./devices');
const a_Encryption = require('../encryption/asymmetric');

const TABLE = 'ep_permissions';
const DEVICE_ID = 'device_id';
const CLIENT_ID = 'client_id';
const DEVICE_KEY = 'device_key';

const CLIENTS_TABLE = 'clients';
const PUBLIC_KEY = 'public_key';
const DISPLAY_NAME = 'display_name';

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
        const action = 'GET PERMISSIONS';
        // assert and hash the device id....
        let deviceIDHash = await DevicesController.assertAndHashDeviceID (req, action); 
        // make sure we received a public key for permissions   
        let client_id = assertBodyKey (req, CLIENT_ID, action);    
        const result = await db.query(`SELECT * FROM ${TABLE} WHERE ${DEVICE_ID} = '${deviceIDHash}' AND ${CLIENT_ID} = '${client_id}';`);
        resp.status(200).json( { has_permissions: result.rows.length > 0 } );
    }
    catch (e) { next(e); }
};

async function assertDeviceAuthAndClientID (req, action) {
    // make sure the device ID and device key match up
    let { deviceIDHash, deviceKey } = await DevicesController.assertDeviceAuth (req, action);
    // make sure we received a public key for permissions   
    let clientID = assertBodyKey (req, CLIENT_ID, action);
    return { deviceIDHash, deviceKey, clientID };
}

module.exports._grant_permissions = async (deviceHash, deviceKey, clientPublicKey, client_id) => {
    // encrypt the device key so that the end party can decrypt it when they need it
    let encryptedDeviceKey = a_Encryption.encryptData(deviceKey, clientPublicKey);
    await db.query(`INSERT INTO ${TABLE} (${DEVICE_ID}, ${CLIENT_ID}, ${DEVICE_KEY}) VALUES ('${deviceHash}', '${client_id}', '${encryptedDeviceKey}');`);
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
        let { deviceIDHash, deviceKey, clientID } = await assertDeviceAuthAndClientID (req, 'GRANT PERMISSIONS');

        // get the public key of the client_id
        const result = await db.query(`SELECT ${PUBLIC_KEY}, ${DISPLAY_NAME} FROM ${CLIENTS_TABLE} WHERE ${CLIENT_ID} = ${clientID};`);
        if (result.rows.length <= 0)
            throw new Error(`Error! [${action}] : Client ID: '${clientID}' doesnt exist!`);
        let clientPublicKey = result.rows[0][PUBLIC_KEY];
        
        await module.exports._grant_permissions(deviceIDHash, deviceKey, clientPublicKey, clientID);
        resp.status(200).json( { message: `Permissions Granted For ${result.rows[0][DISPLAY_NAME]}` } );
    }
    catch (e) { next(e); }
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
module.exports.deny_permissions = async (req, resp, next) => {
    try {
        const action = 'DENY PERMISSIONS';
        let { deviceIDHash, deviceKey, clientID } = await assertDeviceAuthAndClientID (req, action);
        
        const result = await db.query(`SELECT ${DISPLAY_NAME} FROM ${CLIENTS_TABLE} WHERE ${CLIENT_ID} = ${clientID};`);
        if (result.rows.length <= 0)
            throw new Error(`Error! [${action}] : Client ID: '${clientID}' doesnt exist!`);
                
        await db.query(`DELETE FROM ${TABLE} WHERE ${DEVICE_ID} = '${deviceIDHash}' AND ${CLIENT_ID} = '${clientID}';`);
        resp.status(200).json( { message: `Permissions Denied For ${result.rows[0][DISPLAY_NAME]}` } );
    }
    catch (e) { next(e); }
};