/*
    permissions between devices and End Parties
*/
const router = require('express').Router();
const PermissionsController = require('../controllers/permissions');
const checkAuth = require('../middleware/check-auth');
const rateLimiting = require('../middleware/rate-limiting');

router.get      ('/', checkAuth, rateLimiting(.0001, 99999999), PermissionsController.get_permissions);
router.post     ('/', checkAuth, rateLimiting(.0001, 99999999), PermissionsController.grant_permissions);
router.delete   ('/', checkAuth, rateLimiting(.0001, 99999999), PermissionsController.deny_permissions);

module.exports = router;
