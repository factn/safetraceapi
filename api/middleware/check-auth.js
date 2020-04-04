const { db } = require('../controllers/postgresql-utils');
const s_Encryption = require('../encryption/symmetric');
const adminPermissions = require('./admin-permissions');

const TABLE = 'clients';
const API_KEY = 'api_key';

async function getClientByAPIKey (key) {
    key = s_Encryption.encryptData(key, process.env.SAFETRACE_KEY, process.env.SAFETRACE_IV);
    const result = await db.query(`SELECT * FROM ${TABLE} WHERE ${API_KEY} = '${key}';`);
    return result.rows.length > 0 ? result.rows[0] : null;
}

module.exports = async (req, response, next) => {
    try {
        if (adminPermissions(req)) {
            next();
            return;
        }
        let apiKey = req.header(API_KEY);
        if (!apiKey)
            throw new Error('API Key Required!');

        // make sure the api key is valid
        if (!(await getClientByAPIKey(apiKey))) 
            throw new Error('API Key Authorization Failed!');
        
        next();
    }
    catch (e) { next(e); }
};