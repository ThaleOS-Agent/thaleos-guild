import React from "react";

export function MissionFeed() {
  // Placeholder UI; wire to SSE/WebSocket later.
  return (
    <div style={{ border: "1px solid #ddd", borderRadius: 12, padding: 16 }}>
      <div style={{ fontWeight: 700 }}>Live Mission Feed</div>
      <div style={{ marginTop: 8, opacity: 0.8 }}>
        Ready. Add SSE endpoint `/events` in API to stream logs/status.
      </div>
    </div>
  );
}