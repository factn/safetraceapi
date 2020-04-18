/*
    Give Admin Permissions
*/

const API_KEY = 'api_key';
module.exports = function (req) {
    let apiKey = req.header(API_KEY);
    return apiKey && apiKey === process.env.SAFETRACE_API_KEY;
}