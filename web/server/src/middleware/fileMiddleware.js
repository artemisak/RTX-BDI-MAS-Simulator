const { watch, readFileSync } = require("node:fs");
const { resolve } = require("path");
const { sendEventsToAll } = require("./eventsMiddleware");

const watchFolder = resolve(__dirname, "../../../../results");

function watchLogs() {
  watch(watchFolder, (_, fileName) => {
    fileName && readLogFile(fileName);
  });
}

function readLogFile(fileName) {
  const fileData = parseFileData(
    readFileSync(resolve(watchFolder, fileName), "utf-8"),
    fileName
  );
  if (fileData) {
    console.log(fileData);
    sendEventsToAll(fileData);
  }
}

function parseFileData(fileData, fileName) {
  let result;
  const allLines = fileData.split("\n");
  allLines.pop();
  const lastLine = allLines[allLines.length - 1];

  if (!lastLine) return "";
  let lastLineData = lastLine?.split(", ");

  switch (fileName) {
    case "intern.txt":
      result = {
        id: lastLineData[0],
        role: lastLineData[1],
        name: lastLineData[2],
        efficiency: lastLineData[3],
      };
      break;
    case "physician.txt":
      lastLineData = lastLine?.split(", ", 6);
      result = {
        id: lastLineData[0],
        role: lastLineData[1],
        name: lastLineData[2],
        qualification: lastLineData[3],
        workload: lastLineData[4],
        liveQueue: JSON.parse(lastLineData[5]),
        history: JSON.parse(lastLineData[6]),
      };
      break;
    case "patient.txt":
      result = {
        id: lastLineData[0],
        role: lastLineData[1],
        name: lastLineData[2],
        physicianId: lastLineData[3],
        taskUrgency: lastLineData[4],
        taskIntricate: lastLineData[5],
        incomeTime: lastLineData[6],
        resumeTime: lastLineData[7],
      };
      break;
    default:
      result = {};
  }
  return JSON.stringify(result);
}

module.exports = {
  watchLogs,
  readLogFile,
  watchFolder,
};
