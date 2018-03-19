var express = require('express');
var router = express.Router();

// Require controller modules.
var book_controller = require('../controllers/bookController');
var author_controller = require('../controllers/authorController');
// var genre_controller = require('../controllers/genreController');
// var book_instance_controller = require('../controllers/bookinstanceController');

/// BOOK ROUTES ///

// GET catalog home page.
router.get('/', book_controller.index);

// // GET request for one Book.
// router.get('/book/:id', book_controller.book_detail);

// // GET request for list of all Book items.
router.get('/books', book_controller.book_list);

/// AUTHOR ROUTES ///

// // GET request for one Author.
// router.get('/author/:id', author_controller.author_detail);

// // GET request for list of all Authors.
// router.get('/authors', author_controller.author_list);

module.exports = router;