import React from "react";
import { getJSON } from "../api";

export function HealthCard() {
  const [data, setData] = React.useState<any>(null);
  const [err, setErr] = React.useState<string>("");

  React.useEffect(() => {
    getJSON("/health").then(setData).catch((e) => setErr(String(e)));
  }, []);

  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
      <div style={{ fontWeight: 700 }}>Orchestrator Health</div>
      {err && <div style={{ color: "crimson" }}>{err}</div>}
      {data && <pre style={{ margin: 0 }}>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}