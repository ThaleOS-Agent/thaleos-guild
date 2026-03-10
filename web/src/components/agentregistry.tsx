import React from "react";
import { getJSON } from "../api";
import type { AgentRecord } from "../types";

export function AgentRegistry() {
  const [agents, setAgents] = React.useState<AgentRecord[]>([]);
  const [err, setErr] = React.useState("");

  async function refresh() {
    try {
      setErr("");
      const data = await getJSON<AgentRecord[]>("/registry/agents");
      setAgents(data);
    } catch (e) {
      setErr(String(e));
    }
  }

  React.useEffect(() => { refresh(); }, []);

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div style={{ fontWeight: 700 }}>Agent Registry</div>
        <button onClick={refresh}>Refresh</button>
      </div>
      {err && <div style={{ color: "crimson" }}>{err}</div>}
      <div style={{ marginTop: 8 }}>
        {agents.length === 0 ? (
          <div>No agents registered.</div>
        ) : (
          <table width="100%" cellPadding={8}>
            <thead>
              <tr>
                <th align="left">agent_id</th>
                <th align="left">endpoint</th>
                <th align="left">last_seen</th>
              </tr>
            </thead>
            <tbody>
              {agents.map((a) => (
                <tr key={a.agent_id}>
                  <td>{a.agent_id}</td>
                  <td>{a.endpoint || "-"}</td>
                  <td>{new Date(a.last_seen_unix * 1000).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}