from llm import IncidentAnalysisError, analyze_incident 


def main():
    incident = input("Describe the incident: ")

    try:
        report, metrics = analyze_incident(incident)
    except IncidentAnalysisError as error:
        print(f"\nAnalysis failed")
        raise SystemExit(1)

    print("\nIncident analysis:")
    print(report.model_dump_json(indent=2))

    print(
        f"\nMetrics: {metrics.latency_seconds:.2f}s"
        f" | input={metrics.input_tokens}"
        f" | output={metrics.output_tokens}"
        f" | total={metrics.total_tokens}"
    )

    if metrics.request_id:
        print(f"Request ID: {metrics.request_id}")

if __name__ == "__main__":
    main()