/*
    TODO: Update account bio / display name
*/

const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');

const hashing = require('../encryption/hashing');
const a_Encryption = require('../encryption/asymmetric');
const s_Encryption = require('../encryption/symmetric');

const bcrypt = require('bcrypt');
const { v1 } = require('uuid');

const TABLE = 'clients';
const EMAIL = 'email';
const DISPLAY_NAME = 'display_name';
const PASSWORD = 'password';
const BIO = 'bio';
const API_KEY = 'api_key';
const PUBLIC_KEY = 'public_key';
const PRIVATE_KEY = 'private_key';
const CLIENT_ID = 'client_id';

const NEW_PASSWORD = 'new_password';
const NEW_EMAIL = 'new_email';

const SAFETRACE_CLIENT_ID = 1;

const validEmailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

async function getClientByEmail (email) {
    const result = await db.query(`SELECT * FROM ${TABLE} WHERE ${EMAIL} = '${email}';`);
    return result.rows.length > 0 ? result.rows[0] : null;
}

function checkForEmailAndPassword (request, action) {
    let email = assertHeaderKey (request, EMAIL, action);
    let password = assertHeaderKey (request, PASSWORD, action);    
    return { email, password };
}

async function assertClientAuth (request, action) {
    let { email, password } = checkForEmailAndPassword (request, action);
    function throwAuthError () {
        throw new Error(`${action} :: Authorization Failed [Invalid Email Or Password]!`);
    }
    let client = await getClientByEmail(email);
    if (!client) 
        throwAuthError ();
    if (!(await bcrypt.compare(password, client[PASSWORD])))
        throwAuthError ();
    return client;
}


/*
INPUT: { NONE }
OUTPUT
{
    clients: [ 
        { < client object with info > },
        { < client object with info > },
        ...
    ]
}
*/
module.exports.get_clients_list = async (req, response, next) => {
    try {
        let clients = (await db.query(`SELECT ${CLIENT_ID}, ${DISPLAY_NAME}, ${BIO} FROM ${TABLE} WHERE ${CLIENT_ID} != '${SAFETRACE_CLIENT_ID}';`)).rows;
        response.status(200).json( { clients: clients } );
    }
    catch (e) { next(e); }
};


/*
INPUT:
{
    HEADER
    {
        email:      < email >,
        password:   < password >,
    }
    display_name:   < display name >
    bio:            < a short bio >
}
OUTPUT
{
    message:        `Account Created For: < email >, save the API and Private Keys included in this object. Make sure to keep them private and secure`,
    api_key:        < api key >,
    private_key:    < private key >
    public_key:     < public key >
}
*/
module.exports.client_signup = async (req, response, next) => {
    try {
        const action = 'SIGN UP';
        let { email, password } = checkForEmailAndPassword (req, action);
        
        let bio = assertBodyKey (req, BIO, action);
        let displayName = assertBodyKey (req, DISPLAY_NAME, action);
        
        function throwError () {
            throw new Error(`${action} :: Invalid Or Existing Email Address: ${email}`);
        }
        
        if (!validEmailRegex.test(email))
            throwError();
        
        if ((await getClientByEmail(email))) 
            throwError();
            
        const passwordHash = await hashing.hashStringRandom(password);
            
        // make uuid for api key
        let apiKey = await v1(); 
        let encKeys = a_Encryption.getKeyPair();

        let encryptedAPIKey = s_Encryption.encryptData(apiKey, process.env.SAFETRACE_KEY, process.env.SAFETRACE_IV);
        let encryptedPrivateKey = s_Encryption.encryptData(encKeys.privateKey, process.env.SAFETRACE_KEY, process.env.SAFETRACE_IV);

        await db.query(`INSERT INTO ${TABLE} (${EMAIL}, ${DISPLAY_NAME}, ${PASSWORD}, ${BIO}, ${API_KEY}, ${PUBLIC_KEY}, ${PRIVATE_KEY}) VALUES ('${email}', '${displayName}', '${passwordHash}', '${bio}', '${encryptedAPIKey}', '${encKeys.publicKey}', '${encryptedPrivateKey}');`);
        
        // TODO: add a sign in explanation prompt...
        response.status(201).json( { 
            message: `Account Created For: ${email}, save the API and Private Keys included in this object. Make sure to keep them private and secure`,
            api_key: apiKey,
            private_key: encKeys.privateKey,
            public_key: encKeys.publicKey
        } );
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    HEADER
    {
        email:      < email >,
        password:   < password >,
    }
}
OUTPUT
{
    api_key:        < api key >,
    private_key:    < private key >,
    public_key:     < public key >
}
*/
module.exports.recover_api_keys = async (req, response, next) => {
    try {
        let client = await assertClientAuth (req, 'RECOVER API KEYS');
        response.status(201).json( { 
            api_key: s_Encryption.decryptData(client[API_KEY], process.env.SAFETRACE_KEY),
            private_key: s_Encryption.decryptData(client[PRIVATE_KEY], process.env.SAFETRACE_KEY),
            public_key: client[PUBLIC_KEY]
        } );
    }
    catch (e) { next(e); }
};


/*
INPUT:
{
    HEADER
    {
        password:   < password >,
        email:      < email >,
    }
    new_password:   < new password >, OPTIONAL
    new_email:      < new email >,  OPTIONAL
}
OUTPUT
{
    message: `Account Credentials Updated For: < email >`
}
*/
module.exports.update_account_credentials = async (req, response, next) => {
    try {
        let action = 'UPDATE CLIENT CREDENTIALS';
        
        const changingEmail = NEW_EMAIL in req.body;
        const changingPassword = NEW_PASSWORD in req.body;
        
        if ( (!changingEmail) && (!changingPassword) )
            throw new Error(`Error! ${action} :: request body requires either a '${NEW_PASSWORD}' key or '${NEW_EMAIL}' key!`);
        
        let client = await assertClientAuth (req, action);

        let email = changingEmail ? req.body[NEW_EMAIL] : client[EMAIL];
        let pw = changingPassword ? (await hashing.hashStringRandom(req.body[NEW_PASSWORD])) : client[PASSWORD];
            
        await db.query(`UPDATE ${TABLE} SET ${PASSWORD} = '${pw}', ${EMAIL} = '${email}' WHERE ${EMAIL} = '${client[EMAIL]}';`);

        response.status(200).json( { message: `Account Credentials Updated For: ${email}` } );        
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    HEADER
    {
        email:      < email >,
        password:   < password >,
    }
}
OUTPUT:
{
    message: 'Client Account Deleted: < email >'
}
*/
module.exports.delete_client = async (req, response, next) => {
    try {
        let client = await assertClientAuth (req, 'DELETE ACCOUNT');
        await db.query(`DELETE FROM ${TABLE} WHERE ${EMAIL} = '${client[EMAIL]}';`);
        response.status(200).json( { message: `Client Account Deleted: ${client[EMAIL]}` } );
    }
    catch (e) { next(e); }
};
