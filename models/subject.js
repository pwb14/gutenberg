var mongoose = require('mongoose');

var Schema = mongoose.Schema;

var SubjectSchema = new Schema(
  {
    description: {type: String, required: true}
  }
);

// Virtual for book's URL
SubjectSchema
.virtual('url')
.get(function () {
  return '/catalog/subject/' + this._id;
});

//Export model
module.exports = mongoose.model('Subject', SubjectSchema);