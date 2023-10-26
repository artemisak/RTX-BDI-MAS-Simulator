const { constants } = require("../shared/constants");

function eventsHandler(request, response, next) {
  const headers = {
    "Content-Type": "text/event-stream",
    Connection: "keep-alive",
    "Cache-Control": "no-cache",
  };
  response.writeHead(200, headers);

  const data = `data: ${JSON.stringify({})}\n\n`;

  response.write(data);

  const clientId = Date.now();

  const newClient = {
    id: clientId,
    response,
  };

  constants.clients.push(newClient);

  request.on("close", () => {
    console.log(`${clientId} Connection closed`);
    constants.clients = constants.clients.filter(
      (client) => client.id !== clientId
    );
  });
}

function sendEventsToAll(data) {
  constants.clients.forEach((client) => {
    return client.response.write(`data: ${JSON.stringify(data)}\n\n`);
  });
}

module.exports = {
  eventsHandler,
  sendEventsToAll,
};
