const { pool } = require('./postgresql');

const queryKey = 'query';

function getRequestCallback (tableName) {
    return async (request, response, next) => {
        try {
            const columnKey = 'columns';
            let sql = `SELECT ${request.body[columnKey] || '*'} FROM ${tableName}`;
            if (queryKey in request.body)
                sql += ` WHERE ${request.body[queryKey]}`;

            // response.status(200).json( { sql: sql } );
            const queryResult = await pool.query(sql + ';');
            response.status(200).json( { rows: queryResult.rows } );

        }
        catch (e) { next(e); }
    }
}

function deleteRequestCallback (tableName) {
    return async (request, response, next) => {
        try {
            function assertQueryKey () {
                if (!(queryKey in request.body))
                    throw new Error(`Error, DELETE request needs "${queryKey}" key and value for Database query.`);
                return request.body[queryKey];
            }
            const sql = `DELETE FROM ${tableName} WHERE ${assertQueryKey()} RETURNING *;`;

            // response.status(200).json( { sql: sql } );
        
            const queryResult = await pool.query(sql);
            response.status(200).json( { rows: queryResult.rows } );
        }
        catch (e) { next(e); }
    }
}

// adds single qoutes around string arguments for sql queries
function stringifyArg(arg) {
    return typeof arg === 'string' ? `'${arg}'` : arg;
}
// json stringify was hard to read in postman...
function obj2string (obj) {
    return Object.keys(obj).reduce( (t, v) => t + v + ': ' + obj[v] + ', ', '{ ') + '}';
}

function assertBodyKey (key, body, requestType) {
    if (!(key in body))
        throw new Error(`Error! ${requestType} requirse body with key ${key} :: Passed In Body: ${obj2string(body)}`);
}

module.exports = {
    getRequestCallback,
    deleteRequestCallback,
    stringifyArg,
    assertBodyKey,
};