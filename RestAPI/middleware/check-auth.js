const { pool } = require('../controllers/postgresql');
const unlocked = require('./st-unlocker');

const TABLE = 'users';
const APIKEY = 'api_key';
const KEY_HEADER = 'x-api-key';

async function getUserByAPIKey (key) {
    const result = await pool.query(`SELECT * FROM ${TABLE} WHERE ${APIKEY} = '${key}';`);
    return result.rows.length > 0 ? result.rows[0] : null;
}

module.exports = async (req, response, next) => {
    try {
        if (unlocked(req)) {
            next();
            return;
        }

        function throwError () {
            throw new Error('API Key Authorization Failed!');
        }

        let apiKey = req.header(KEY_HEADER);
        if (!apiKey)
            throwError();
        
        // make sure the api key is valid
        let user = await getUserByAPIKey(apiKey)
        if (!user) 
            throwError();
        
        next();
    }
    catch (e) { next(e); }
};