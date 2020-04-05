const { db } = require('../controllers/postgresql-utils');
const s_Encryption = require('../encryption/symmetric');
const adminPermissions = require('./admin-permissions');
const consts = require('../controllers/constants');

async function getClientByAPIKey (key) {
    let { iv, data } = s_Encryption.splitIVData(key);
    key = s_Encryption.encryptData(data, process.env.SAFETRACE_KEY, iv);
    const result = await db.query(`SELECT * FROM ${consts.CLIENTS_TABLE} WHERE ${consts.API_KEY} = '${key}';`);
    return result.rows.length > 0 ? result.rows[0] : null;
}

module.exports = async (req, response, next) => {
    try {
        if (adminPermissions(req)) {            
            req.st_client = (await db.query(`SELECT * FROM ${consts.CLIENTS_TABLE} WHERE ${consts.CLIENT_ID} = ${consts.SAFETRACE_CLIENT_ID};`)).rows[0];
            next();
            return;
        }
        let apiKey = req.header(consts.API_KEY);
        if (!apiKey)
            throw new Error('API Key Required!');

        // make sure the api key is valid
        let client = await getClientByAPIKey(apiKey);
        if (!client) 
            throw new Error('API Key Authorization Failed!');
        req.st_client = client;
        next();
    }
    catch (e) { next(e); }
};