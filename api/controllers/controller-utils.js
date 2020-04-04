// json stringify was hard to read in postman...
function obj2string (obj) {
    return Object.keys(obj).reduce( (t, v) => t + v + ': ' + obj[v] + ', ', '{ ') + '}';
}
function assertBodyKey (request, key, action) {
    if (!(key in request.body))
        throw new Error(`Error! ${action} requires body with key ${key} :: Passed In Body: ${obj2string(request.body)}`);
    return request.body[key];
}
function assertHeaderKey (request, key, action) {
    let value = request.header(key);
    if (!value)
        throw new Error (`Error [${action}]: '${key}' must be included in the request header.`);
    return value;
}

module.exports = { assertBodyKey, assertHeaderKey };