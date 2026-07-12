export type BridgeState = {
  workspaceRoot: string;
  intent: string;
  allowWrite: boolean;
};

export async function runBridgeAgent(state: BridgeState): Promise<string> {
  const mode = state.allowWrite ? "read-write" : "read-only";
  return `[Mastra Bridge] intent="${state.intent}" scope="${state.workspaceRoot}" mode="${mode}"`;
}

