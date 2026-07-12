from __future__ import annotations

from typing import Literal, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph


class GraphState(TypedDict, total=False):
    request: str
    draft: str
    violations: list[str]
    attempts: int
    approved: bool


def draft_node(state: GraphState) -> GraphState:
    attempts = state.get("attempts", 0) + 1
    base = "Production deployment plan with rollback + observability controls."
    if attempts == 1:
        draft = "Deploy now."
    else:
        draft = base
    return {"attempts": attempts, "draft": draft}


def validate_node(state: GraphState) -> GraphState:
    violations: list[str] = []
    draft = state.get("draft", "")
    if "rollback" not in draft.lower():
        violations.append("Missing rollback strategy.")
    if "observability" not in draft.lower():
        violations.append("Missing observability plan.")
    return {"violations": violations, "approved": len(violations) == 0}


def revise_node(state: GraphState) -> GraphState:
    violations = state.get("violations", [])
    revised = state.get("draft", "")
    if "Missing rollback strategy." in violations:
        revised += " Add rollback procedure."
    if "Missing observability plan." in violations:
        revised += " Add observability checks."
    return {"draft": revised}


def human_review_node(state: GraphState) -> GraphState:
    # In production this node receives an operator decision from an external channel.
    return state


def route_from_validation(state: GraphState) -> Literal["human_review", "revise", "end"]:
    if state.get("approved", False):
        return "human_review"
    if state.get("attempts", 0) >= 3:
        return "end"
    return "revise"


def route_from_human(_: GraphState) -> Literal["end"]:
    return "end"


def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("draft", draft_node)
    graph.add_node("validate", validate_node)
    graph.add_node("revise", revise_node)
    graph.add_node("human_review", human_review_node)

    graph.add_edge(START, "draft")
    graph.add_edge("draft", "validate")
    graph.add_conditional_edges(
        "validate",
        route_from_validation,
        {"human_review": "human_review", "revise": "revise", "end": END},
    )
    graph.add_edge("revise", "draft")
    graph.add_conditional_edges("human_review", route_from_human, {"end": END})

    return graph.compile(
        checkpointer=MemorySaver(),
        interrupt_before=["human_review"],
    )


if __name__ == "__main__":
    app = build_graph()
    initial_state: GraphState = {
        "request": "Generate deployment runbook for service-x.",
        "attempts": 0,
    }
    config = {"configurable": {"thread_id": "deployment-runbook-demo"}}
    first_pass = app.invoke(initial_state, config=config)
    print(first_pass)

