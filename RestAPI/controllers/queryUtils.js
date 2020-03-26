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
    assertBodyKey,
};