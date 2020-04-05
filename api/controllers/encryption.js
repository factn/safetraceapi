/*
    TEMPORARY ENDPOINT TO ENCRYPT DATA
    (SINCE EVENTUALLY ENCRYPTION SHOULD BE END-TO-END)
*/

const { assertBodyKey, assertHeaderKey } = require('./controller-utils');

const consts = require('./constants');
const hashing = require('../encryption/hashing');
const s_Encryption = require('../encryption/symmetric');
const a_Encryption = require('../encryption/asymmetric');
const DevicesController = require('./devices');

function assertRange (request, key, min, max, action) {
    let value = assertBodyKey (request, key, action);
    if (value < min || value > max)
        throw new Error(`Event '${key}' Must Be In Range (${min}, ${max})`);
}

function assertEventFormats (request) {
    let action = 'ASSSERT EVENT FORMATTING';

    assertBodyKey (request, consts.DEVICE_ID, action);
    assertRange (request, consts.ROW_TYPE, 0, 2, action);
    // GPS
    if (request.body[consts.ROW_TYPE] === 0) {
        assertRange (request, consts.LONGITUDE, -180, 180, action + ' FOR GPS DATA');
        assertRange (request, consts.LATITUDE, -90, 90, action + ' FOR GPS DATA');
    }
    // BLUETOOTH
    else if (request.body[consts.ROW_TYPE] === 1) {
        assertBodyKey (request, consts.CONTACT_ID, action + ' FOR BLUETOOTH DATA');
        assertBodyKey (request, consts.CONTACT_LEVEL, action + ' FOR BLUETOOTH DATA');
    }
    // SURVEY
    else if (request.body[consts.ROW_TYPE] === 2) {
        assertBodyKey (request, consts.SYMPTOMS, action + ' FOR SURVEY DATA');
        assertRange (request, consts.INFECTION_STATUS, 0, 3, action + ' FOR SURVEY DATA');
    }
}

/*
HEADER (for all)
{
    device_key: < device-private-key >
}
    
GPS DATA = 
{
    device_id:  < device-id >,
    row_type:   0, // integer 0 - 2 [0: GPS] [1: BlueTooth] [2: Survey]
    latitude:   < -90 to 90 float range >,
    longitude:  < -180 to 180 float range >
}
BLUETOOTH DATA = 
{
    device_id:      < device-id >,
    row_type:       1, // integer 0 - 2 [0: GPS] [1: BlueTooth] [2: Survey]
    contact_id:     < contacted-device-id >,
    contact_level:  < signal-strength-float >
}
SURVEY DATA = 
{
    device_id:          < device-id >,
    row_type:           2, // integer 0 - 2 [0: GPS] [1: BlueTooth] [2: Survey]
    symptoms:           < comma seperated string of symptoms >,
    infection_status:   < integer 0 - 3 [0 opt out] [1 dont know] [2 infected] [3 recovered] >
}
OUTPUT
{
    encrypted_body: < an object with all the proper keys encrypted to send to the event data table >
}
*/

const entropyDelim = '%%$$%%';

module.exports.encrypt_event = async (req, response, next) => {
    try {
        // the encrypted version of the event data to send to the API
        let postBody = {};
        assertEventFormats(req);

        // make sure the device ID and device key match up and are valid
        let { deviceIDHash, deviceKey } = await DevicesController.assertDeviceIDAndKey (req, 'ENCRYPT EVENT');
        
        postBody[consts.DEVICE_ID] = deviceIDHash;
        postBody[consts.ROW_TYPE] = req.body[consts.ROW_TYPE];

        // add some entropy, so encrypted values cant be inferred from other rows
        function addEntropy(value) {
            return String(value) + entropyDelim + postBody[consts.DEVICE_ID]
        }
        
        // Encrypt the data with the device key
        // GPS
        if (req.body[consts.ROW_TYPE] === 0) {
            postBody[consts.LONGITUDE] = s_Encryption.encryptData(addEntropy(req.body[consts.LONGITUDE]), deviceKey);
            postBody[consts.LATITUDE] = s_Encryption.encryptData(addEntropy(req.body[consts.LATITUDE]), deviceKey);   
        }
        // BLUETOOTH
        else if (req.body[consts.ROW_TYPE] === 1) {
            // hash the contact id
            postBody[consts.CONTACT_ID] = await hashing.hashString(String(req.body[consts.CONTACT_ID]));
            postBody[consts.CONTACT_LEVEL] = s_Encryption.encryptData(addEntropy(req.body[consts.CONTACT_LEVEL]), deviceKey);   
        }
        // SURVEY
        else if (req.body[consts.ROW_TYPE] === 2) {
            postBody[consts.SYMPTOMS] = s_Encryption.encryptData(addEntropy(req.body[consts.SYMPTOMS]), deviceKey);   
            postBody[consts.INFECTION_STATUS] = s_Encryption.encryptData(addEntropy(req.body[consts.INFECTION_STATUS]), deviceKey);   
        }
        
        response.status(201).json( { encrypted_body: postBody } );
    }
    catch (e) { next(e); }
}

/*
INPUT: [ NONE ]
OUTPUT
{
    private_key:    < private key >
    public_key:     < public key >
}
*/
module.exports.obtain_keys = async (req, response, next) => {
    try {
        let encKeys = a_Encryption.getKeyPair();
        response.status(200).json( { 
            private_key: encKeys.privateKey,
            public_key: encKeys.publicKey
        } );
    }
    catch (e) { next(e); }
};
