

const { db } = require('./postgresql-utils');
const { assertBodyKey, assertHeaderKey } = require('./controller-utils');

const NODE_ID = 'node_id';
const TRIPLE_ID = 'triple_id';
const SHARE = 'share';

const TRIPLES_TABLE = 'triples';

/*
REQUEST
{
    node_id: integer,
    triple_id: string,
    share: string,
}
*/
module.exports.postTriple = async (request, response, next) => {
    try {

        // assert the request body format
        const action = 'Post Triple';
        let triple_id = assertBodyKey (request.body, TRIPLE_ID, action);
        let node_id = assertBodyKey (request.body, NODE_ID, action);
        let share = assertBodyKey (request.body, SHARE, action);
        
        // insert triple into DB
        await db.query(`INSERT INTO ${TRIPLES_TABLE} (${NODE_ID}, ${TRIPLE_ID}, ${SHARE}) VALUES (${node_id}, '${triple_id}', '${share}');`);
        
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
        triple_id: string
    }
    OUTPUT
    {
        share: string
    }
*/
module.exports.getTriple = async (request, response, next) => {
    try {
        // assert request body format
        const action = 'Get Triple';
        let triple_id = assertBodyKey (request.body, TRIPLE_ID, action);
        let node_id = assertBodyKey (request.body, NODE_ID, action);

        // retreive the triple and delete it from the DB
        const result = await db.query(`DELETE FROM ${TRIPLES_TABLE} WHERE ${NODE_ID} = ${node_id} AND ${TRIPLE_ID} = '${triple_id}' RETURNING ${SHARE};`);
        if (result.rowCount <= 0) 
            throw new Error(`No Triple Found With ID: ${triple_id} For NodeID: ${node_id}`)
        
        response.status(200).json( result.rows[0] );
    }
    catch (e) { next(e); }
};

