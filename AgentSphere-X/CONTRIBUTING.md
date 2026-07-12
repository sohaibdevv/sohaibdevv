# Contributing to AgentSphere-X

Thanks for helping build a state-of-the-art open-source multi-agent reference.

## Engineering Principles

1. Keep **core agent logic** separate from **tool transport/adapters**.
2. Favor **typed boundaries** (Pydantic models, TypeScript interfaces) over ad-hoc dictionaries.
3. Make agent behavior **observable** (structured traces, deterministic IDs, reproducible evals).
4. Preserve **determinism** in orchestrators when possible; isolate non-deterministic model behavior.

## Repository Standards

- `agents/` holds runtime logic and orchestration patterns.
- `mcp-servers/` holds protocol-facing tool adapters.
- `apps/web/` hosts UI and API integration surfaces.
- `evals/` stores benchmark matrices and scenario fixtures.

When adding a new capability, update both runtime code and eval coverage.

## Pull Request Workflow

1. Fork and create a focused branch.
2. Add or update implementation with tests/eval fixtures.
3. Run local quality checks (lint, type-check, tests, smoke run).
4. Open a PR with architecture notes and risk boundaries.

PRs are reviewed for:

- Correctness and safety
- Architectural fit
- Test/eval quality
- Documentation completeness

## Adding a New Persona

To contribute a new persona, include:

1. **Persona spec** in code comments/docstring: role, goals, constraints, tool budget.
2. **State model** definition (typed schema and transition invariants).
3. **Memory strategy** (short-term, long-term, retrieval integration).
4. **Tool access policy** (allowed tools + rationale).
5. **Evaluation scenario** in `evals/scenarios/`.

A persona PR is incomplete without an executable scenario and expected outcome criteria.

## Code Style

- Python: typed function signatures, explicit return contracts, minimal side effects.
- TypeScript: strict mode, explicit interfaces, no untyped `any` in public surfaces.
- Keep modules small and composable; avoid framework lock-in in business logic.

## Security & Responsible Development

- Never commit secrets or private credentials.
- Enforce least-privilege access for MCP tools.
- Document unsafe operations and guard them with approvals/human checkpoints.

We value deeply engineered contributions over large unreviewable diffs.

