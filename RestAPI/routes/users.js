/*
    the API users, or tracking apps
*/
const router = require('express').Router();
const UsersController = require('../controllers/users');
const rateLimiting = require('../middleware/rate-limiting');

router.post     ('/', rateLimiting(24, 2), UsersController.user_signup);
router.get      ('/', rateLimiting(24, 2), UsersController.recover_api_key);
router.patch    ('/', rateLimiting(24, 2), UsersController.update_account_credentials);
router.delete   ('/', rateLimiting(24, 1), UsersController.delete_user);

module.exports = router;