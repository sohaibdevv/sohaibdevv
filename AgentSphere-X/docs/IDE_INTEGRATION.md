# IDE Integration (MCP-First)

AgentSphere-X is designed for modern agentic IDEs (Claude Code, Cursor, Copilot CLI, terminal agents) through **Model Context Protocol (MCP)**.

## Integration Model

1. **Agent runtimes** (LangGraph/CrewAI/PydanticAI/Mastra) stay pure and testable.
2. **Tool bridges** are exposed through MCP servers in `mcp-servers/`.
3. IDE agents connect to MCP endpoints and invoke tools with strict schemas.

## Supported Local Workflows

### Claude Code / Cursor

- Register local MCP servers from this repository (filesystem and dev API).
- Allow read-only filesystem operations by default; enable write scopes per workspace.
- Route execution traces to local logs (`.logs/agent-traces/*.jsonl`) for replay.

### Terminal Agents

- Start MCP servers locally and keep agent runtime in-process for deterministic debugging.
- Use thread IDs when invoking LangGraph to preserve checkpoint history.
- Use typed input payloads for PydanticAI interfaces to fail fast on invalid requests.

## Safety & Debugging

- **Least privilege:** tool scopes are narrowed by repository root and endpoint allowlists.
- **Traceability:** every agent run should emit `run_id`, `thread_id`, tool call list, and latency metrics.
- **Deterministic replay:** LangGraph checkpoints + eval scenario fixtures in `evals/scenarios`.

## Recommended Local Boot Sequence

1. Install Python and Node dependencies.
2. Start MCP servers under `mcp-servers/*`.
3. Launch `apps/web` for dashboard-based orchestration.
4. Execute smoke tests via `scripts/smoke_test.py`.
5. Run benchmark packs with `scripts/run_evals.py`.

## MCP Contract Pattern

Each MCP tool should expose:

- Strict JSON schema for input/output
- Non-ambiguous error envelopes
- Idempotency guidance for mutating operations
- Structured logs with correlation IDs

This keeps agent behavior predictable across IDEs and CI environments.

