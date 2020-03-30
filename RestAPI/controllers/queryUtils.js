// json stringify was hard to read in postman...
function obj2string (obj) {
    return Object.keys(obj).reduce( (t, v) => t + v + ': ' + obj[v] + ', ', '{ ') + '}';
}
function assertBodyKey (key, body, action) {
    if (!(key in body))
        throw new Error(`Error! ${action} requires body with key ${key} :: Passed In Body: ${obj2string(body)}`);
}
module.exports = { assertBodyKey };