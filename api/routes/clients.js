/*
    Client: the API users, or tracking apps
*/
const router = require('express').Router();
const ClientsController = require('../controllers/clients');
const rateLimiting = require('../middleware/rate-limiting');

router.get      ('/',       rateLimiting(.0001, 999999), ClientsController.get_clients_list);
router.post     ('/',       rateLimiting(.0001, 999999), ClientsController.client_signup);
router.patch    ('/',       rateLimiting(.0001, 999999), ClientsController.update_account_credentials);
router.delete   ('/',       rateLimiting(.0001, 999999), ClientsController.delete_client);
router.get      ('/keys',   rateLimiting(.0001, 999999), ClientsController.recover_api_keys);

module.exports = router;
