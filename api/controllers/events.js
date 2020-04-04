
const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');

const a_Encryption = require('../encryption/asymmetric');
const s_Encryption = require('../encryption/symmetric');

const DevicesController = require('./devices');

const TABLE = 'events';
const EVENT_ID = 'event_id';
const DEVICE_ID = 'device_id';
const ROW_TYPE = 'row_type';
const BLUETOOTH_ROW_TYPE = 1;

const LONGITUDE = 'longitude';
const LATITUDE = 'latitude';

const CONTACT_ID = 'contact_id';
const CONTACT_LEVEL = 'contact_level';

const INFECTION_STATUS = 'infection_status';
const SYMPTOMS = 'symptoms';

const PRIVATE_KEY = 'private_key';
const PUBLIC_KEY = 'public_key';
const PERMISSIONS_TABLE = 'ep_permissions';
const DEVICE_KEY = 'device_key';

const CLIENTS_TABLE = 'clients';
const CLIENT_ID = 'client_id';

async function filterRows (rows, clientID) {
    let permissions = (await db.query(`SELECT * FROM ${PERMISSIONS_TABLE} WHERE ${CLIENT_ID} = ${clientID};`)).rows;

    function deviceIDGavePermission (deviceID) {
        return permissions.some( (p) => p[DEVICE_ID] === deviceID );
    }

    // filter for only rows where device gave permission
    rows = rows.filter( (e) => deviceIDGavePermission(e[DEVICE_ID]) );

    // filter for bluetooth rows that have a contactID that gave permission
    rows = rows.filter( (e) => e[ROW_TYPE] !== BLUETOOTH_ROW_TYPE || deviceIDGavePermission(e[CONTACT_ID]) );

    return { rows, permissions }
}

async function decryptRows (rows, permissions, EP_privateKey) {
    permissions.forEach ( (p) => {
        p.deviceKey = a_Encryption.decryptData(p[DEVICE_KEY], EP_privateKey);
    });

    function getDeviceKey (deviceID) {
        return permissions.find( p => p[DEVICE_ID] === deviceID).deviceKey;
    }

    const entropyDelim = '%%$$%%';
    function removeEntropy(strData) {
        return strData.split(entropyDelim)[0];
    }

    rows.forEach ( (r) => {
        let deviceKey = getDeviceKey(r[DEVICE_ID]);
        // GPS
        if (r[ROW_TYPE] === 0) {
            r[LONGITUDE] = Number(removeEntropy(s_Encryption.decryptData(r[LONGITUDE], deviceKey)));
            r[LATITUDE] = Number(removeEntropy(s_Encryption.decryptData(r[LATITUDE], deviceKey)));   
        }
        // BLUETOOTH
        else if (r[ROW_TYPE] === 1) {
            r[CONTACT_LEVEL] = Number(removeEntropy(s_Encryption.decryptData(r[CONTACT_LEVEL], deviceKey)));   
        }
        // SURVEY
        else if (r[ROW_TYPE] === 2) {
            r[SYMPTOMS] = removeEntropy(s_Encryption.decryptData(r[SYMPTOMS], deviceKey));   
            r[INFECTION_STATUS] = Number(removeEntropy(s_Encryption.decryptData(r[INFECTION_STATUS], deviceKey)));   
        }
    });
}

/*
INPUT:
{   
    HEADER 
    {
        private_key: < EP's private key >
    }
    public_key: < EP's public key >
    columns:    < comma seperated column names >  // (OPTIONAL, default is all)
    query:      < an SQL query >                  // (OPTIONAL)
}
OUTPUT: array of rows returned
{
    rows: [ 
        { < row object with columns as keys > },
        { < row object with columns as keys > },
        ...
    ]
}
*/
module.exports.get_events = async (req, response, next) => {
    try {
        let action = 'GET EVENTS';
        let EP_publicKey = assertBodyKey (req, PUBLIC_KEY, action);
        let EP_privateKey = assertHeaderKey(req, PRIVATE_KEY, action);
    
        let clientsQuery = await db.query(`SELECT ${CLIENT_ID} FROM ${CLIENTS_TABLE} WHERE ${PUBLIC_KEY} = '${EP_publicKey}';`);
        if (clientsQuery.rows.length <= 0) 
            throw new Error('Error! No client ID associated with public key');
        let clientID = clientsQuery.rows[0][CLIENT_ID];
        
        const QUERY = 'query';
        const COLUMNS = 'columns';
        let sql = `SELECT ${req.body[COLUMNS] || '*'} FROM ${TABLE}`;
        if (QUERY in req.body)
            sql += ` WHERE ${req.body[QUERY]}`;

        const result = await db.query(sql + ';');
        
        // filter out rows with device ids that havent given permission
        let { rows, permissions } = await filterRows (result.rows, clientID);
        
        // now we need to decrypt the ROs key with the EPs private key, in order to decrypt the ROs data
        await decryptRows (rows, permissions, EP_privateKey);
        
        response.status(200).json( { rows: rows } );
    }
    catch (e) { next(e); }
};


/*
ASSUMES REQUEST BODY HAS ALREADY BEEN ENCRYPTED:

TODO: figure out a way to assert it was encrypted....

INPUT
{
    HEADER 
    {
        device_key: < device-private-key >
    }
    the already encrypted post body that was returned form the encryption endpoint
}
OUTPUT
{
    event_id: < event_id integer created for the row >
}
*/
module.exports.post_event = async (req, response, next) => {
    try { 
        // just make sure we're only posting if we have the device key
        await DevicesController.assertDeviceAuthHashed (req, 'POST EVENT');
        
        // adds single qoutes around string arguments for sql queries
        function stringifyArg(arg) {
            return typeof arg === 'string' ? `'${arg}'` : arg;
        }

        let keys = Object.keys(req.body);
        
        // format the values for sql
        let values = keys.map(k => stringifyArg(req.body[k])).join(',');    
        // format the keys for sql columns
        let columns = keys.join(", ");   

        // add the event row
        const result = await db.query(`INSERT INTO ${TABLE} (${columns}) VALUES (${values}) RETURNING ${EVENT_ID};`);
        response.status(201).json( result.rows[0] );
    }
    catch (e) { next(e); }
}