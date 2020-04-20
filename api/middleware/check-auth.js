const adminPermissions = require('./admin-permissions');

const API_KEY = 'api_key';

module.exports = async (req, response, next) => {
    try {
        let apiKey = req.header(API_KEY);
        if (!apiKey)
            throw new Error('API Key Required!');
        
        if (adminPermissions(req)) {            
            next();
            return;
        }
        throw new Error('API Key Authorization Failed!');
    }
    catch (e) { next(e); }
};