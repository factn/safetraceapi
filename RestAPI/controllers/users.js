// TODO: options returns all columns in mini doc...
const { pool } = require('./postgresql');
const queryUtils = require('./queryUtils');

const table = 'users';
const userID = 'user_id';
const userInfo = 'phone_number';

/*
INPUT:
{
    'columns': 'user_id, phone_number' // comma seperated column names (optional, default is all)
    'query': 'user_id = 0'     // an SQL query (optional)
}
OUTPUT: array of rows returned
{
    rows: [ 
        { user_id: x, phone_number: xxxxxx }, 
        { user_id: y, phone_number: yyyyyy }, 
        ...
    ]
}
*/
module.exports.get_users = queryUtils.getRequestCallback(table);

/*
INPUT:
{
    'phone_number': 15553332222 // phone number with country code
}
OUTPUT
{
    'user_id': user_id integer created for user with phone number
}
*/
module.exports.post_user = async (request, response, next) => {
    try {
        queryUtils.assertBodyKey (userInfo, request.body, 'POST');
        let sql = `INSERT INTO ${table} (${userInfo}) VALUES (${request.body[userInfo]}) RETURNING ${userID};`;
        const queryResult = await pool.query(sql);
        response.status(201).json( queryResult.rows[0] );
    }
    catch (e) { next(e); }
};

/*
INPUT:
{
    'user_id': 0,               // the user id to update
    'phone_number': 15553332222 // phone number with country code to update
}
OUTPUT
{
    'user_id': 0,               // the user id updated
    'phone_number': 15553332222 // updated phone number
}
*/
module.exports.patch_user = async (request, response, next) => {
    try {
        queryUtils.assertBodyKey (userID, request.body, 'PATCH');
        queryUtils.assertBodyKey (userInfo, request.body, 'PATCH');
        
        let sql = `UPDATE ${table} SET ${userInfo} = ${request.body[userInfo]} WHERE ${userID} = ${request.body[userID]} RETURNING *`;
        const queryResult = await pool.query(sql);
        response.status(200).json( queryResult.rows[0] );        
    }
    catch (e) { next(e); }
};

/*
INPUT
{
    'user_id': 0 // user id to delete
}
OUTPUT user row deleted
{
    'user_id': 0,               
    'phone_number': 15553332222 
}
*/
module.exports.delete_user = async (request, response, next) => {
    try {
        queryUtils.assertBodyKey (userID, request.body, 'DELETE');
        const sql = `DELETE FROM ${table} WHERE ${userID} = ${request.body[userID]} RETURNING *;`;
        const queryResult = await pool.query(sql);
        response.status(200).json( queryResult.rows[0] );
    }
    catch (e) { next(e); }
};
