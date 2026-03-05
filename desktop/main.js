// ===================================
// ThaléOS Electron Main Process (optional)
// ===================================
const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: false,
      contextIsolation: true
    },
    title: "ThaléOS AI Chat"
  });

  mainWindow.loadFile(path.join(__dirname, "public/index.html"));
  mainWindow.on("closed", () => (mainWindow = null));
}

app.on("ready", createWindow);
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
app.on("activate", () => {
  if (mainWindow === null) createWindow();
});

// ===================================
// IPC: Bridge Commands to local Python orchestrator (optional)
// ===================================
ipcMain.on("invoke-agent", (event, agentName, payload) => {
  console.log(`🟢 [IPC] Received invoke-agent: ${agentName}`, payload);

  const scriptPath = path.join(__dirname, "../core/orchestrator.py");
  const gatekeeper = spawn("python3", [scriptPath, agentName, JSON.stringify(payload)]);

  gatekeeper.stdout.on("data", (data) => event.reply("agent-response", data.toString()));
  gatekeeper.stderr.on("data", (data) => event.reply("agent-response", `Error: ${data.toString()}`));
  gatekeeper.on("error", (err) => event.reply("agent-response", `Agent process failed: ${err.message}`));
});
