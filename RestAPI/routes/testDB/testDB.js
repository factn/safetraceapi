// TODO: options returns all columns in mini doc...

const express = require('express');
const router = express.Router();

const { pool } = require('../postgresql');

const mainTable = 'main_table';
/*
event_id SERIAL PRIMARY KEY,
*/

const eventIDColumn = 'event_id';
const allCols = ['user_id', 'encryption', 'time', 'location_type', 'location', 'symptoms'];

const queryKey = 'query';

// adds single qoutes around string arguments for sql queries
function stringifyArg(arg) {
    return typeof arg === 'string' ? `'${arg}'` : arg;
}

// handle get requests
router.get('/', async (request, response, next) => {
    try {
        const columnKey = 'columns';

        let sql = `SELECT ${request.body[columnKey] || "*"} FROM ${mainTable}`;
        
        if (queryKey in request.body)
            sql += ` WHERE ${request.body[queryKey]}`;
            
        const queryResult = await pool.query(sql + ';');
        response.status(200).json( queryResult.rows );
    }
    catch (e) { next(e); }
});

// handle post requests
router.post('/', async (request, response, next) => {
    try {

        // response.status(201).json( request.body );
        
        const allColsStr = "(" + allCols.join(", ") + ")";
        const postValuesKey = 'values';

        if (!(postValuesKey in request.body))
            throw new Error("[POST] Error! request body must have a 'values' key holding an array of JSON objects to append");
        

        // json stringify was hard to read in postman...
        function obj2string (obj) {
            return Object.keys(obj).reduce( (t, v) => t + v + ': ' + obj[v] + ', ', '{ ') + '}';
        }
        function checkObjForAllColumns (obj) {
            // TODO: check value types....
            allCols.forEach( k => {
                // throw new Error(JSON.stringify(obj, null, ''));
                if (!(k in obj))
                    throw new Error(`[POST] Error! each element appended must contain keys: ${allColsStr} :: Missing Key: '${k}' in object: ${obj2string(obj)}`);
            });
        }
        
        let objsToAppend = request.body[postValuesKey];
        objsToAppend.forEach ( o => checkObjForAllColumns(o) );
        
        let sql = `INSERT INTO ${mainTable} ${allColsStr} VALUES ` + objsToAppend.map(o=>`(${allCols.map(k=>stringifyArg(o[k])).join(',')})`).join(',') + `RETURNING ${eventIDColumn};`;
        
        const queryResult = await pool.query(sql);

        // returns an object per instert where obj = { "event_id": event_id created for insert }
        response.status(201).json( queryResult.rows );
    }
    catch (e) { next(e); }
});

function getUpdateSQLArgs (body) {
    let r = [];
    for (let k in body) {
        if (k === queryKey) 
            continue;
        if (!allCols.includes(k))
            throw new Error('Error, invalid UPDATE request body key: ' + k);
        r.push(`${k} = ${stringifyArg(body[k])}`);
    }
    return r.join(',');
}

function assertQueryKey (request, body) {
    if (!queryKey in body)
        throw new Error(`Error, ${request} request needs "${queryKey}" key and value for Database SQL query.`);
    return body[queryKey];
}
    
// handle patch requests
router.patch('/', async (request, response, next) => {
    try {
        let query = assertQueryKey('UPDATE', request.body);

        let sqlKeysArgs = getUpdateSQLArgs(request.body);
        
        let sql = `UPDATE ${mainTable} SET ${sqlKeysArgs} WHERE ${query}`;
        
        const queryResult = await pool.query(sql);
        response.status(200).json( queryResult );
    }
    catch (e) { next(e); }
});

// handle delete requests
router.delete ('/', async (request, response, next) => {
    try {
        let query = assertQueryKey('DELETE', request.body);

        const sql = `DELETE FROM ${mainTable} WHERE ${query}`;
        // const sql = `DELETE FROM ${mainTable}` // delete all
        
        const queryResult = await pool.query(sql);
        response.status(200).json( queryResult );
    }
    catch (e) { next(e); }
});

module.exports = router;