const { pool } = require('./postgresql');
const queryUtils = require('./queryUtils');
const bcrypt = require('bcrypt');
const { v1 } = require('uuid');

const TABLE = 'users';
const EMAIL = 'email';
const PASSWORD = 'password';
const APIKEY = 'api_key';

const validEmailRegex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

async function getUserByEmail (email) {
    const result = await pool.query(`SELECT * FROM ${TABLE} WHERE ${EMAIL} = '${email}';`);
    return result.rows.length > 0 ? result.rows[0] : null;
}

function checkForEmailAndPassword (requestBody, action) {
    queryUtils.assertBodyKey (EMAIL, requestBody, action);
    queryUtils.assertBodyKey (PASSWORD, requestBody, action);    
}
function throwAuthError (action) {
    throw new Error(`${action} :: Authorization Failed [Invalid Email Or Password]!`);
}
async function authorizePassword (request, action, user) {
    let passwordMatch = await bcrypt.compare(request.body[PASSWORD], user[PASSWORD]);
    if (!passwordMatch)
        throwAuthError (action);
}
async function assertUserExists (action, request) {
    let user = await getUserByEmail(request.body[EMAIL]);
    if (!user) 
        throwAuthError (action);
    return user;
}
async function assertUserAuth (action, request) {
    let user = await assertUserExists (action, request);
    await authorizePassword (request, action, user);
    return user;
}


/*
INPUT:
{
    'email': appUsingAPI@site.com,
    'password': 'password'
}
OUTPUT
{
    message: `Account Created For: appUsingAPI@site.com, save the API Key included in this object`,
    apiKey: 'The-api-key....'
}
*/
module.exports.user_signup = async (req, response, next) => {
    try {
        const action = 'SIGN UP';
        checkForEmailAndPassword (req.body, action);

        let email = req.body[EMAIL];
        
        function throwError () {
            throw new Error(`${action} :: Invalid Or Existing Email Address: ${email}`);
        }
        
        if (!validEmailRegex.test(email))
            throwError();
        
            
        let user = await getUserByEmail(email);
        if (user) 
            throwError();
            
        const passwordEnc = await bcrypt.hash(req.body[PASSWORD], Number(process.env.BCRYPT_SALT));
        
        // make uuid for api key
        let apiKey = await v1(); 
                
        const r = await pool.query(`INSERT INTO ${TABLE} (${EMAIL}, ${PASSWORD}, ${APIKEY}) VALUES ('${email}', '${passwordEnc}', '${apiKey}');`);
        
        // TODO: add a sign in explanation prompt...
        response.status(201).json( { 
            message: `Account Created For: ${email}, save the API Key included in this object`,
            apiKey: apiKey
        } );
    }
    catch (e) { next(e); }
};



/*
INPUT:
{
    'email': appUsingAPI@site.com,
    'password': 'password'
}
OUTPUT
{
    apiKey: 'The-api-key....'
}
*/
module.exports.recover_api_key = async (req, response, next) => {
    try {
        const action = 'RECOVER API KEY';
        checkForEmailAndPassword (req.body, action);
        let user = await assertUserAuth (action, req);
        response.status(201).json( { apiKey: user[APIKEY] } );
    }
    catch (e) { next(e); }
};


/*
INPUT:
{
    'email': appUsingAPI@site.com,
    'password': 'password',
    'newPassword': 'password2', OPTIONAL
    'newEmail': somenewemail',  OPTIONAL
}
OUTPUT
{
    message: `Account Credentials Updated For: [UPDATED EMAIL]`
}
*/
module.exports.update_account_credentials = async (req, response, next) => {
    try {
        let action = 'UPDATE USER CREDENTIALS';
        checkForEmailAndPassword (req.body, action);
        const newPasswordKey = 'newPassword';
        const newEmailKey = 'newEmail';

        const changingPassword = newPasswordKey in req.body;
        const changingEmail = newEmailKey in req.body;
        
        if ( (!changingPassword) && (!changingEmail) )
            throw new Error(`Error! ${action} :: request body requires either a '${newPasswordKey}' key or '${newEmailKey}' key!`);
        
        let user = await assertUserAuth (action, req);

        let email = changingEmail ? req.body[newEmailKey] : user[EMAIL];
        
        let pw = user[PASSWORD];
        if (changingPassword) 
            pw = await bcrypt.hash(req.body[newPasswordKey], Number(process.env.BCRYPT_SALT));
            
        let r = await pool.query(`UPDATE ${TABLE} SET ${PASSWORD} = '${pw}', ${EMAIL} = '${email}' WHERE ${EMAIL} = '${user[EMAIL]}';`);

        response.status(200).json( { message: `Account Credentials Updated For: ${email}` } );        
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    'email': appUsingAPI@site.com,
    'password': 'password'
}
OUTPUT:
{
    message: User Account Deleted: appUsingAPI@site.com
}
*/
module.exports.delete_user = async (req, response, next) => {
    try {
        let action = 'DELETE ACCOUNT';
        checkForEmailAndPassword (req.body, action);
        let user = await assertUserAuth (action, req);
        const r = await pool.query(`DELETE FROM ${TABLE} WHERE ${EMAIL} = '${req.body[EMAIL]}';`);
        response.status(200).json( { message: `User Account Deleted: ${req.body[EMAIL]}` } );
    }
    catch (e) { next(e); }
};
