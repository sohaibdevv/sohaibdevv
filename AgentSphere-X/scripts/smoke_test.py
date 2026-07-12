from agents.python.crewai.enterprise_ops_crew import describe_enterprise_ops_crew
from agents.python.langgraph.cyclic_validator import build_graph


def run() -> None:
    crew_meta = describe_enterprise_ops_crew()
    app = build_graph()
    result = app.invoke(
        {"request": "Generate deployment runbook for service-x.", "attempts": 0},
        config={"configurable": {"thread_id": "smoke-test-thread"}},
    )
    print({"crew": crew_meta["persona"], "graph_approved": result.get("approved", False)})


if __name__ == "__main__":
    run()

