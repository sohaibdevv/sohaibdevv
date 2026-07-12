# AgentSphere-X

Production-grade reference repository for 2026 multi-agent engineering:
LangGraph, CrewAI, Microsoft Agent Framework, PydanticAI, smolagents, and Mastra + MCP.

## Repository Structure

```text
AgentSphere-X/
├─ .github/
│  └─ workflows/
│     ├─ ci.yml
│     └─ release.yml
├─ agents/
│  ├─ python/
│  │  ├─ crewai/
│  │  │  └─ enterprise_ops_crew.py
│  │  ├─ langgraph/
│  │  │  └─ cyclic_validator.py
│  │  ├─ pydanticai/
│  │  │  └─ typed_workflow.py
│  │  ├─ microsoft_agent_framework/
│  │  │  └─ blueprint.py
│  │  └─ smolagents/
│  │     └─ code_first_loop.py
│  └─ typescript/
│     └─ mastra/
│        └─ bridge-agent/
│           └─ agent.ts
├─ apps/
│  └─ web/
│     ├─ app/
│     │  ├─ page.tsx
│     │  └─ api/
│     │     └─ chat/
│     │        └─ route.ts
│     └─ package.json
├─ mcp-servers/
│  ├─ local-fs/
│  │  └─ server.ts
│  └─ dev-api/
│     └─ server.ts
├─ evals/
│  ├─ benchmark.matrix.yaml
│  └─ scenarios/
│     ├─ crew-enterprise-regression.yaml
│     └─ langgraph-determinism.yaml
├─ docs/
│  └─ IDE_INTEGRATION.md
├─ scripts/
│  ├─ run_evals.py
│  └─ smoke_test.py
├─ CONTRIBUTING.md
└─ pyproject.toml
```

## Multi-Agent Personas

### Persona A — Enterprise Operations Crew (CrewAI)
- **Framework:** CrewAI
- **State:** Shared structured task context + role-local scratchpads
- **Memory:** Episodic run logs persisted per workflow and retrievable by ticket ID
- **Tools:** ERP connector, SLA policy retriever, approval gateway, audit logger
- **Pattern:** Declarative role-based crews (`FinanceOps`, `LegalOps`, `PeopleOps`) with explicit handoff contracts

### Persona B — Deterministic Graph Engineer (LangGraph)
- **Framework:** LangGraph
- **State:** Typed state dictionary with deterministic transitions and attempt counters
- **Memory:** Checkpointed time-travel state via checkpointer; replayable branches
- **Tools:** Static validators, policy checks, diff analyzers
- **Pattern:** Cyclic validation/revision loop + `interrupt_before` human checkpoint for regulated decisions

### Persona C — Full-Stack Bridge Agent (Mastra + MCP)
- **Framework:** Mastra (TypeScript/Next.js-native)
- **State:** Session-scoped typed context synchronized with UI and API routes
- **Memory:** Short-term session memory + durable workspace-level memory adapters
- **Tools:** MCP filesystem server, local API inspector, Git-aware code intelligence tools
- **Pattern:** Live IDE-coupled copiloting from web dashboard into local repos and dev endpoints

## Core Snippet 1: Type-Safe PydanticAI Workflow

See `agents/python/pydanticai/typed_workflow.py`.

```python
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
```

This workflow enforces strict input/output boundaries and rejects invalid schemas before and after model execution.

## Core Snippet 2: Cyclic LangGraph Validator

See `agents/python/langgraph/cyclic_validator.py`.

```python
from langgraph.graph import StateGraph, START, END
```

This graph implements deterministic retry loops with explicit validation gates and human interrupts.

## Quick Start

1. Install Python dependencies:
   - `pip install -e .`
2. Run typed workflow sample:
   - `python agents/python/pydanticai/typed_workflow.py`
3. Run LangGraph cyclic sample:
   - `python agents/python/langgraph/cyclic_validator.py`
