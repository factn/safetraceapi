/*
    temporary encryption endpoint
*/
const router = require('express').Router();
const EncryptionController = require('../controllers/encryption');
const checkAuth = require('../middleware/check-auth');
const rateLimiting = require('../middleware/rate-limiting');

router.post ('/', checkAuth, rateLimiting(.0001, 99999999), EncryptionController.encrypt_event);
router.get  ('/', rateLimiting(.0001, 99999999), EncryptionController.obtain_keys);

module.exports = router;