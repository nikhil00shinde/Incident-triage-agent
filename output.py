from base import IncidentReport

def display_report(report: IncidentReport) -> None:
    print(f"\nSeverity: {report.severity}")
    print(f"Summary: {report.summary}")


    print(f"\nObserved evidence")
    for item in report.observed_evidence:
        print(f"- {item}")

    print("\nHypotheses:")
    for hypothesis in report.hypotheses:
        print(f" Evidence: {hypothesis.cause} [{hypothesis.confidence}]")

        for evidence in hypothesis.supporting_evidence:
            print(f" Evidence: {evidence}")

    print(f"\nImmediate actions:")
    for action in report.immediate_actions:
        print(f"- {action}")

    print("\nMissing informations:")
    for item in report.missing_information:
        print(f"- {item}")


    