/*
    devices registered with api
*/

const router = require('express').Router();
const DevicesController = require('../controllers/devices');
const checkAuth = require('../middleware/check-auth');
const rateLimiting = require('../middleware/rate-limiting');

router.get      ('/', checkAuth, rateLimiting(.0001, 99999999), DevicesController.is_device_registered);
router.post     ('/', checkAuth, rateLimiting(.0001, 99999999), DevicesController.register_device);
router.delete   ('/', checkAuth, rateLimiting(.0001, 99999999), DevicesController.unregister_device);

module.exports = router;