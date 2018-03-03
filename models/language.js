var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var LanguageSchema = new Schema(
  {
    iso_639_1: {type: String, max: 2, required: true},
    iso_639_2: {type: String, max: 3, required: false},
    name : {type: String, max: 100, required: true}
  }
);

// Virtual for book's URL
LanguageSchema
.virtual('url')
.get(function () {
  return '/catalog/language/' + this._id;
});

//Export model
module.exports = mongoose.model('Language', LanguageSchema);