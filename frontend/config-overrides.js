const path = require('path');  // Use require instead of import
const dotenv = require('dotenv');  // Use require for dotenv

// Load environment variables from the custom path
dotenv.config({ path: path.resolve(__dirname, '../configuration/.env') });

module.exports = function override(config, env) {
  // Custom Webpack configuration (if necessary)
  return config;
};
