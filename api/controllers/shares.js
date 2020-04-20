

const { v1 } = require('uuid');
const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');
const ComputationIDs = require('./computation-id');

const SHARES = 'shares';
const NODE_ID = 'node_id';
const SHARE = 'share';

const DEVICE_ID = 'device_id';
const COMPUTATION_ID = 'computation_id';

const SHARES_TABLE = 'shares';


/*
    REQUEST 
    {
        shares: [
            {
                node_id: integer,
                share : string,
            },
            { ... },
            { ... },
        ]
    }
*/

module.exports.postShares = async (request, response, next) => {
    try {
        // assert request body format
        const action = 'Post Shares';
        
        let shares = assertBodyKey (request.body, SHARES, action);
        if (!Array.isArray(shares)) 
            throw new Error(`Error! [${action}]: ${SHARES} key must be an array`);

        for (let i = 0; i < shares.length; i++) {
            assertBodyKey (shares[i], NODE_ID, action);
            assertBodyKey (shares[i], SHARE, action);
        }

        // generate device id
        let deviceID = await v1(); 

        // get computation id (current hour)
        let computation_id = ComputationIDs.getCurrentComputationIDForClientPost();
        
        // sql values list comma seperated
        let valuesSQL = shares.map( (s) => `('${computation_id}', ${s[NODE_ID]}, '${deviceID}', '${s[SHARE]}')` ).join (', ');
        
        // add shares to DB
        await db.query(`INSERT INTO ${SHARES_TABLE} (${COMPUTATION_ID}, ${NODE_ID}, ${DEVICE_ID}, ${SHARE}) VALUES ${valuesSQL};`);
        
        response.status(201).json( { 
            status: "OK"
        } );
    }
    catch (e) { next(e); }
};


/*
    REQUEST
    {
        node_id: integer
    }
    OUTPUT
    {
        computation_id: string,
        shares: [
            {
                device_id: string,
                share: string
            },
            { ... },
            { ... },
        ]
    }
*/
module.exports.getShares = async (request, response, next) => {
    try {
        // assert request body format
        const action = 'Get Shares';
        let node_id = assertBodyKey (request.body, NODE_ID, action);

        // get computation id (computation id's for shares that were posted the previous hour)
        let computation_id = ComputationIDs.getCurrentComputationIDForMPCGet();
        
        // get the shares for the computation id and node id
        const result = await db.query(`SELECT ${DEVICE_ID}, ${SHARE} FROM ${SHARES_TABLE} WHERE ${COMPUTATION_ID} = '${computation_id}' AND ${NODE_ID} = ${node_id};`);
        
        response.status(200).json( { 
            computation_id: computation_id,
            shares: result.rows
        } );
    }
    catch (e) { next(e); }
};
