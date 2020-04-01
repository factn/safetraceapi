/*
    the API users, or tracking apps
*/
const router = require('express').Router();
const UsersController = require('../controllers/users');
const rateLimiting = require('../middleware/rate-limiting');

router.post     ('/', rateLimiting(.0001, 999999), UsersController.user_signup);
router.get      ('/', rateLimiting(.0001, 999999), UsersController.recover_api_key);
router.patch    ('/', rateLimiting(.0001, 999999), UsersController.update_account_credentials);
router.delete   ('/', rateLimiting(.0001, 999999), UsersController.delete_user);

module.exports = router;