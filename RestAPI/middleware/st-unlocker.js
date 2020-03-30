
module.exports = function (req) {
    return (
        process.env.ST_UNLOCKER_KEY && 
        process.env.ST_UNLOCKER && 
        req.header(process.env.ST_UNLOCKER_KEY) && 
        req.header(process.env.ST_UNLOCKER_KEY) === process.env.ST_UNLOCKER
    );
}