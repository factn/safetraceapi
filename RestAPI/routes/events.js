// TODO: options returns all columns in mini doc...
const router = require('express').Router();
const EventsController = require('../controllers/events');

router.get('/', EventsController.get_events);

router.post('/', EventsController.post_event);
  
module.exports = router;