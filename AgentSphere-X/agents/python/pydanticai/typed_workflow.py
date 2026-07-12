from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


class TicketInput(BaseModel):
    ticket_id: str = Field(min_length=5, max_length=32)
    team: Literal["finance", "legal", "people", "security"]
    priority: Literal["low", "medium", "high", "critical"]
    summary: str = Field(min_length=10, max_length=500)
    requires_approval: bool = False


class TicketResolution(BaseModel):
    owner_role: str
    action_plan: list[str] = Field(min_length=1, max_length=6)
    escalation_required: bool
    confidence: float = Field(ge=0.0, le=1.0)


@dataclass
class RuntimeDeps:
    policy_store: dict[str, str]


resolver_agent = Agent(
    "openai:gpt-4.1-mini",
    deps_type=RuntimeDeps,
    result_type=TicketResolution,
    system_prompt=(
        "You route enterprise tickets. "
        "Always return valid JSON matching TicketResolution."
    ),
)


@resolver_agent.tool
def get_policy(ctx: RunContext[RuntimeDeps], team: str) -> str:
    return ctx.deps.policy_store.get(team, "Use global baseline policy.")


def route_ticket(ticket: TicketInput, deps: RuntimeDeps) -> TicketResolution:
    validated_ticket = TicketInput.model_validate(ticket)
    prompt = (
        f"Ticket {validated_ticket.ticket_id}\n"
        f"Team: {validated_ticket.team}\n"
        f"Priority: {validated_ticket.priority}\n"
        f"Requires approval: {validated_ticket.requires_approval}\n"
        f"Summary: {validated_ticket.summary}\n"
        "Return a compliant routing decision."
    )
    run = resolver_agent.run_sync(prompt, deps=deps)
    return TicketResolution.model_validate(run.data)


if __name__ == "__main__":
    deps = RuntimeDeps(
        policy_store={
            "finance": "Finance approvals require dual-signoff over $50k.",
            "legal": "Legal requests need clause risk categorization.",
            "people": "People operations incidents require privacy triage.",
            "security": "Critical security tickets page the on-call responder.",
        }
    )
    sample = TicketInput(
        ticket_id="INC-84291",
        team="security",
        priority="critical",
        summary="Unusual IAM role escalations were detected in production logs.",
        requires_approval=True,
    )
    print(route_ticket(sample, deps).model_dump_json(indent=2))

