const { watch, readFileSync, readFile } = require("node:fs");
const { resolve } = require("path");
const { sendEventsToAll } = require("./eventsMiddleware");

const watchFolder = resolve(__dirname, "../../../../Results");
const groups = {
  "intern.json": "Intern",
  "patient.json": "Patient",
  "physician.json": "Physician",
};

function watchLogs() {
  watch(watchFolder, (_, fileName) => {
    fileName && readLogFile(fileName);
  });
}

function readLogFile(fileName) {
  const controller = new AbortController();
  const signal = controller.signal;
  readFile(
    resolve(watchFolder, fileName),
    {
      signal,
      encoding: "utf-8",
    },
    (err, data) => {
      console.log(fileName);
      if (data.trim().length === 0) controller.abort();

      sendEventsToAll({ group: groups[fileName], data });
    }
  );
}

module.exports = {
  watchLogs,
  readLogFile,
};
