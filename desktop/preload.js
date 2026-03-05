const { contextBridge, ipcRenderer } = require("electron");

const listeners = new Set();

contextBridge.exposeInMainWorld("thaleos", {
  invokeAgent: (agent, payload) => ipcRenderer.send("invoke-agent", agent, payload),
  onAgentResponse: (callback) => {
    const handler = (_event, data) => callback(data);
    listeners.add({ callback, handler });
    ipcRenderer.on("agent-response", handler);
  },
  removeAgentResponseListener: (callback) => {
    for (const item of Array.from(listeners)) {
      if (item.callback === callback) {
        ipcRenderer.removeListener("agent-response", item.handler);
        listeners.delete(item);
      }
    }
  }
});
