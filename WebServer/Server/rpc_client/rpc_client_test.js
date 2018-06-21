var client = require('./rpc_client');

client.getNewsSummariesForUser('test_user', 1, function(response) {
  console.assert(response != null);
});
