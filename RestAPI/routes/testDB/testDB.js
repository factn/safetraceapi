const express = require('express');
const router = express.Router();



const { pool } = require('../postgresql');

// const {Client} = require('pg');


const mainTable = 'main_table';

function buildSQLTemplateParams (c) {
    let r = [];
    for (let i = 0; i < c; i++)
        r.push('$' + (i + 1));
    return '(' + r.join(', ') + ')';
}
/*
event_id SERIAL PRIMARY KEY,
user_id, encryption, time, location_type, location, symptoms
*/

const allColumns = ['user_id', 'encryption', 'time', 'location_type', 'location', 'symptoms'];

const queryString = 'query';



function checkBodyForPost (body) {
    allColumns.forEach( k => {
        if (!(k in body))
            throw new Error(postBodyErrorMsg + " :: Missing Key: " + k);
    });
    // TODO: check value types....
    // return allColumns.every( k => k in body );
}
function buildParamsFromPostBody(body) {
    return Object.keys(body).map( k => body[k] );
}


async function queryPostgres(sql, params) {
    // const client = new Client();
    // await client.connect();
    // return await client.query(sql, params);

    return await pool.query(sql, params);
}

const columnKey = 'column';

// handle get requests
router.get('/', async (request, response, next) => {
    try {
        
        let sql = `SELECT ${request.body[columnKey] || "*"} FROM ` + mainTable;
        if (queryString in request.body)
            sql += 'WHERE ' + request.body[queryString];
        // sql += ';';
        
        const queryResult = await queryPostgres(sql + ';');

        response.status(200).json( queryResult.rows );
    }
    catch (e) { next(e); }
});

// handle post requests
const postParamsString = "(" + allColumns.join(", ") + ")";
const postSQL = `INSERT INTO ${mainTable} ${postParamsString} VALUES ${buildSQLTemplateParams(allColumns.length)}`;
const postBodyErrorMsg = "Error! POST request body must contain keys:" + postParamsString;

router.post('/', async (request, response, next) => {
    try {

        // let body = {
        //     user_id: '0',
        //     time: '00:12:16',
        //     latitude: '-165.556',
        //     longitude: '45.05',
        // };

        // if (!
            checkBodyForPost(request.body);//)
            // throw new Error(postBodyErrorMsg);

        const params = buildParamsFromPostBody(request.body);
        
        // TODO: Get event id back
        const queryResult = await queryPostgres(postSQL, params);

        response.status(201).json( queryResult );
    }
    catch (e) { next(e); }
});


function getUpdateSQLTemplate (body) {
    let r = [[],[]];
    let i = 1;
    for (let k in body) {
        if (k === queryString) 
            continue;

        if (!allColumns.includes(k))
            throw new Error('Error, invalid UPDATE request body key: ' + k);

        r[0].push(`${i++} = ${i++}`);
        r[1].push(k);
        r[1].push(body[k]);
    }
    r[0] = r[0].join(', ')
    return r;

    // for (let i = 0; i < c; i++)
    //     r.push('$' + (i + 1));
    // return '(' + r.join(', ') + ')';
}


function checkBodyForQueryString (request, body) {
    if (!queryString in body)
        throw new Error(`Error, ${request} request needs "${queryString}" key and value for Database SQL query.`);
    return body[queryString];
}

    
// handle patch requests
router.patch('/', async (request, response, next) => {
    try {

        let query = checkBodyForQueryString('UPDATE', request.body);

        // if (!queryString in request.body)
        //     throw new Error('Error, UPDATE request needs "query" value for Database SQL query.');

        let r = getUpdateSQLTemplate(request.body);
        let sqlTemplate = r[0];
        let sqlKeysArgs = r[1];

        // const client = new Client();
        // await client.connect();
    
        // get row first
        // let sql = `SELECT * FROM ${mainTable} WHERE event_id = $1`;
        // let params = [0];
        // const qResult = await client.query(sql, params);
        // if (qResult.rowCount === 0)
        //     throw new Error("No Event ID ....");

        

        //multiple
        let sql = `UPDATE ${mainTable} SET ${sqlTemplate} WHERE ${query}`;
        // params = [
        //     'time', '1:36:00',
        //     'user_id', '55',
        //     [0]
        // ];

        const queryResult = await pool.query(sql, sqlKeysArgs);

        
        // const params = [body.user_id, body.time, body.latitude, body.longitude];
        // const params = [0];
        
        // const queryResult = await queryPostgres(sql, params);

        response.status(200).json( queryResult );
    }
    catch (e) { next(e); }
});

// handle delete requests
router.delete ('/', async (request, response, next) => {
    try {

        let query = checkBodyForQueryString('DELETE', request.body);

        const sql = `DELETE FROM ${mainTable} WHERE ${query}`;
        
        // delete all
        // const sql = 'DELETE FROM "mainTable"';
        // const params = [0];
        
        
        const queryResult = await queryPostgres(sql, params);

        response.status(200).json( queryResult );
    }
    catch (e) { next(e); }
});

module.exports = router;