var client = require('./rpc_client');

client.add(1, 99, function(response) {
    console.assert(response == 100);
});
