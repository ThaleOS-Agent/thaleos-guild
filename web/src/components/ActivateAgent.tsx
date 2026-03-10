import React from "react";
import { postJSON } from "../api";

export function ActivateAgent() {
  const [agentId, setAgentId] = React.useState("utilix-local-1");
  const [command, setCommand] = React.useState("activate");
  const [out, setOut] = React.useState<any>(null);
  const [err, setErr] = React.useState("");

  async function send() {
    try {
      setErr("");
      setOut(null);
      const res = await postJSON("/orchestrator/activate", {
        agent_id: agentId,
        command,
        payload: { note: "hello from Guild Console" }
      });
      setOut(res);
    } catch (e) {
      setErr(String(e));
    }
  }

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
      <div style={{ fontWeight: 700 }}>Activate Agent</div>
      <div style={{ display: "flex", gap: 8, marginTop: 8, flexWrap: "wrap" }}>
        <input value={agentId} onChange={(e) => setAgentId(e.target.value)} placeholder="agent_id" />
        <input value={command} onChange={(e) => setCommand(e.target.value)} placeholder="command" />
        <button onClick={send}>Send</button>
      </div>
      {err && <div style={{ color: "crimson", marginTop: 8 }}>{err}</div>}
      {out && <pre style={{ marginTop: 8 }}>{JSON.stringify(out, null, 2)}</pre>}
    </div>
  );
}