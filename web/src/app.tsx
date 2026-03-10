import React from "react";
import { Layout } from "./components/Layout";
import { HealthCard } from "./components/HealthCard";
import { AgentRegistry } from "./components/AgentRegistry";
import { ActivateAgent } from "./components/ActivateAgent";
import { MissionFeed } from "./components/MissionFeed";

export default function App() {
  return (
    <Layout>
      <div style={{ display: "grid", gap: 16 }}>
        <HealthCard />
        <AgentRegistry />
        <ActivateAgent />
        <MissionFeed />
      </div>
    </Layout>
  );
}