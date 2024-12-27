module.exports = {
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: 'reports',
      outputName: 'frontend-test-results.xml'
    }]
  ]
};

