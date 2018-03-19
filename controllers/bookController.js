var Book = require('../models/book');
var Author = require('../models/author');
var Language = require('../models/language');
var Subject = require('../models/subject');

var async = require('async');

exports.index = function(req, res) {   
    
    async.parallel({
        book_count: function(callback) {
            Book.count(callback);
        },
        author_count: function(callback) {
            Author.count(callback);
        },
        language_count: function(callback) {
            Language.count(callback);
        },
        subject_count: function(callback) {
            Subject.count(callback);
        },
    }, function(err, results) {
        res.render('index', { title: 'Gutenberg Books', error: err, data: results });
    });
};

// Display list of all Books.
exports.book_list = function(req, res, next) {

  Book.find({}, 'title author')
    .populate('author')
    .exec(function (err, list_books) {
      if (err) { return next(err); }
      //Successful, so render
      res.render('book_list', { title: 'Book List', book_list: list_books });
    });
    
};