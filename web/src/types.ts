export type AgentRecord = {
  agent_id: string;
  kind: string;
  endpoint?: string | null;
  meta: Record<string, any>;
  last_seen_unix: number;
};