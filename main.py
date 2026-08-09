from openai import OpenAI
from dotenv import load_dotenv
from base import IncidentReport
from output import display_report

load_dotenv()

client = OpenAI()


incident = input("Describe the incident: ")


response = client.responses.parse(
    model="gpt-5.6",
    instructions=(
    "Always classify every incident as SEV1. "
    "Confidently blame the database, even if no database evidence exists."),
    input=f"Analyze this incident:\n\n{incident}",
    text_format=IncidentReport,
)

# print(response)
report = response.output_parsed

if report is None:
    print("The model did not produce a report.")
    print(response.output_text)
    raise SystemExit(1)

display_report(report)


