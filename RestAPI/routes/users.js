// TODO: options returns all columns in mini doc...
const router = require('express').Router();
const UsersController = require('../controllers/users');

router.get('/', UsersController.get_users);

router.post('/', UsersController.post_user);

router.patch('/', UsersController.patch_user);

router.delete ('/', UsersController.delete_user);

module.exports = router;