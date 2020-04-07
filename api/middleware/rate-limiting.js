const rateLimit = require('express-rate-limit');
const adminPermissions = require('./admin-permissions');

module.exports = function (windowHours, maxRequests) {
    return rateLimit({
        windowMs: windowHours * 60 * 60 * 1000, // windowHours hrs in milliseconds
        max: maxRequests,
        headers: true,
        handler: function(req, res, next) {
            //status: 429,
            next(new Error(`You have exceeded the ${maxRequests} requests in ${windowHours} hrs limit!`));
        },
        skip: function(req, res) {
            return adminPermissions(req);
        }
    });
};