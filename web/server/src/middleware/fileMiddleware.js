const { watch, readFileSync } = require("node:fs");
const { resolve } = require("path");

const watchFolder = resolve(__dirname, "../../../../results");

function watchLogs() {
  watch(watchFolder, (eventType, fileName) => {
    fileName && readLogFile(fileName);
  });
}

function readLogFile(fileName) {
  const data = readFileSync(resolve(watchFolder, fileName), "utf-8");
  console.log(data);
}

module.exports = {
  watchLogs,
};
