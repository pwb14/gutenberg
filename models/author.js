var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var AuthorSchema = new Schema(
  {
    name: {type: String, required: true, max: 100},
    date_of_birth: {type: String},
    date_of_death: {type: String},
    wiki_link: {type: String, required: false, max: 100},
  }
);

// Virtual for author's URL
AuthorSchema
.virtual('url')
.get(function () {
  return '/catalog/author/' + this._id;
});

//Export model
module.exports = mongoose.model('Author', AuthorSchema);