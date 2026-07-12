from pathlib import Path


def run() -> None:
    scenarios = sorted(Path("evals/scenarios").glob("*.yaml"))
    print(f"Loaded {len(scenarios)} evaluation scenario(s).")
    for scenario in scenarios:
        print(f"- {scenario.name}")


if __name__ == "__main__":
    run()

