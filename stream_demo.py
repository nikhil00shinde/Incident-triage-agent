from time import perf_counter

from openai import OpenAI

from base import IncidentReport
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

incident = input("Describe the incident: ")
started_at = perf_counter()
first_delta_at = None


with client.responses.stream(
    model="gpt-5.6",
    instructions=(
        "Analyze only the provided evidence. Do not invent facts. "
        "Use UNKNOWN when severity cannot be determined."
    ),
    input=incident,
    text_format=IncidentReport,
) as stream:
    print("\n Streaming raw JSON:\n")

    for event in stream:
        if event.type == "response.output_text.delta":
            if first_delta_at is None:
                first_delta_at = perf_counter()

            print(event.delta,end="", flush=True)

        elif event.type == "response.refusal.delta":
            print(event.delta,end="",flush=True)

        elif event.type == "response.error":
            print(f"\nStreaming error: {event.error}")

    final_response = stream.get_final_response()


total_time = perf_counter() - started_at
report = final_response.output_parsed


if report is None:
    raise RuntimeError("No parsed incident report was returned.")


print("\n\nValidated Pydantic object:")
print(report)



if first_delta_at is not None:
    first_output_time = first_delta_at - started_at
    print(f"\nTime to first output: {first_output_time:.2f}s")

print(f"Total time: {total_time:.2f}s")
