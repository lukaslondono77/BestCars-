const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const reviews = new Schema({
	id: {
    type: Number,
    required: true,
	},
	name: {
    type: String,
    required: true
  },
  dealership: {
    type: Number,
    required: true,
  },
  review: {
    type: String,
    required: true
  },
  purchase: {
    type: Boolean,
    required: true
  },
  purchaseDate: {
    type: String,
    required: true
  },
  carMake: {
    type: String,
    required: true
  },
  carModel: {
    type: String,
    required: true
  },
  carYear: {
    type: Number,
    required: true
  },
});

module.exports = mongoose.model('reviews', reviews);
