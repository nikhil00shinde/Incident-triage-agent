from dataclasses import dataclass

from llm import IncidentAnalysisError, analyze_incident

@dataclass(frozen=True)

class EvalCase:
    name: str
    incident: str
    expected_severity: str 

CASES = [
    EvalCase(
        "Vague report",
        "env error in the project",
        "UNKNOWN",
    ),
    EvalCase(
        "total outpage",
        "The production API is unavailable for all users worldwide.",
        "SEV1",
    ),
    EvalCase(
        "partial checkout outage",
        "Forty percent of production checkout requests return HTTP 500.",
        "SEV2",
    ),
    EvalCase(
        "major latency",
        "All production users see eight-second latency, but requests complete.",
        "SEV2",
    ),
    EvalCase(
        "small search failure",
        "Search fails for 5% of users, and refreshing succeeds.",
        "SEV3",
    ),
    EvalCase(
        "single customer",
        "One customer has delayed webhooks; manual retry works.",
        "SEV3",
    ),
    EvalCase(
        "local environment",
        "A developer's local .env file is missing. Production is healthy.",
        "SEV4",
    ),
    EvalCase(
        "staging failure",
        "The staging deployment failed. Production remains healthy.",
        "SEV4",
    ),
    EvalCase(
        "unknown impact",
        "Production CPU usage is high. No user-impact information was provided.",
        "UNKNOWN",
    ),
]

def main():
    passed = 0 
    total_tokens = 0 
    total_latency = 0.0 


    for index, case in enumerate(CASES, start=1):
        try:
            report, metrics = analyze_incident(case.incident)

            severity_correct = report.severity == case.expected_severity 
            evidence_present = bool(report.observed_evidence)
            summary_present = bool(report.summary.strip())


            case_passed = (
                severity_correct
                and evidence_present
                and summary_present
            )

            total_tokens += metrics.total_tokens
            total_latency += metrics.latency_seconds


            if case_passed:
                passed += 1 
                status = "PASS"
            else:
                status = "FAIL"

            print(
                f"{index:02}. {status} | {case.name} | "
                f"expected={case.expected_severity} | "
                f"actual={report.severity} | "
                f"{metrics.latency_seconds:.2f}s"
            )

        except IncidentAnalysisError as error:
            print(f"{index:02}. ERROR | {case.name} | {error}")

    print("\nEvaluation summary")
    print(f"Passed: {passed}/{len(CASES)}")
    print(f"Pass rate: {passed / len(CASES):.0%}")
    print(f"Average latency: {total_latency / len(CASES):.2f}s")
    print(f"Total tokens: {total_tokens}")



if __name__ == "__main__":
    main()