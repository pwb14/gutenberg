var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var BookSchema = new Schema(
  {
    title: {type: String, required: true},
    author: {type: Schema.ObjectId, ref: 'Author', required: true},
    language: {type: Schema.ObjectId, ref: 'Language', required: true},
    subjects: [ {type: Schema.ObjectId, ref: 'Subject'}],
    number: {type: Number, required: true},
    // fileHash: {type}
    // summary: {type: String, required: true},
    // published date
  },
  {collection: 'book'}
);

// Virtual for book's URL
BookSchema
.virtual('url')
.get(function () {
  return '/catalog/book/' + this._id;
});

//Export model
module.exports = mongoose.model('Book', BookSchema);