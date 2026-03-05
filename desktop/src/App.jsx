import React, { useEffect, useRef, useState } from "react";

export default function App() {
  const [chatMessages, setChatMessages] = useState([
    { role: "system", content: "Welcome to ThaléOS. How can I assist you today?" }
  ]);
  const [chatInput, setChatInput] = useState("");
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  useEffect(() => {
    const handleAgentResponse = (data) => {
      setChatMessages((prev) => [...prev, { role: "assistant", content: data }]);
    };

    window.thaleos?.onAgentResponse(handleAgentResponse);
    return () => window.thaleos?.removeAgentResponseListener?.(handleAgentResponse);
  }, []);

  const sendChatMessage = () => {
    if (!chatInput.trim()) return;

    const userMessage = { role: "user", content: chatInput };
    setChatMessages((prev) => [...prev, userMessage]);

    // Keyword-based routing (placeholder)
    let agent = "sagequery";
    let payload = { query: chatInput };

    if (chatInput.toLowerCase().includes("scan")) {
      agent = "utilix";
      payload = { task: "scan_system" };
    } else if (chatInput.toLowerCase().includes("generate report")) {
      agent = "scribe";
      payload = { action: "generate_report", content: chatInput };
    }

    window.thaleos?.invokeAgent(agent, payload);
    setChatInput("");
  };

  return (
    <div style={{ fontFamily: "system-ui", display: "flex", flexDirection: "column", height: "100vh" }}>
      <header style={{ padding: 16, borderBottom: "1px solid #333" }}>
        <h1 style={{ margin: 0, fontSize: 18 }}>ThaléOS AI</h1>
      </header>

      <main style={{ flex: 1, overflowY: "auto", padding: 16 }}>
        <div style={{ maxWidth: 900, margin: "0 auto" }}>
          {chatMessages.map((m, i) => (
            <div key={i} style={{ marginBottom: 14, display: "flex", justifyContent: m.role === "user" ? "flex-end" : "flex-start" }}>
              <div style={{
                padding: 12,
                borderRadius: 10,
                maxWidth: 600,
                background: m.role === "user" ? "#1f6feb" : "#222",
                color: "#fff"
              }}>
                <div style={{ fontWeight: 700, marginBottom: 6 }}>{m.role === "user" ? "You" : "ThaléOS"}</div>
                <div>{m.content}</div>
              </div>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>
      </main>

      <footer style={{ padding: 16, borderTop: "1px solid #333" }}>
        <div style={{ maxWidth: 900, margin: "0 auto", display: "flex", gap: 8 }}>
          <input
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendChatMessage()}
            placeholder="Ask ThaléOS anything..."
            style={{ flex: 1, padding: 10, borderRadius: 10, border: "1px solid #333", background: "#111", color: "#fff" }}
          />
          <button onClick={sendChatMessage} style={{ padding: "10px 14px", borderRadius: 10, border: "1px solid #333" }}>
            Send
          </button>
        </div>
      </footer>
    </div>
  );
}
