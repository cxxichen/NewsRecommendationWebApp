const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const UserSchema = new mongoose.Schema({
  email: { type: String, index: { unique: true }},
  password: { type: String }
});


UserSchema.methods.comparePassword = function comparePassword(password, callback) {
  bcrypt.compare(password, this.password, callback);
};

UserSchema.pre('save', function saveHook(next) {
  const user = this;

  // proceed further only if the password is modified or the user is new
  if (!user.isModified('password')) return next();

  // generate a salt
  return bcrypt.genSalt((saltError, salt) => {
    if (saltError) { return next(saltError); }

    // hash the password using the generated salt
    return bcrypt.hash(user.password, salt, (hashError, hash) => {
      if (hashError) { return next(hashError); }
      // replace a password string with hash value
      user.password = hash;
      return next();
    });
  });
});

module.exports = mongoose.model('User', UserSchema);
