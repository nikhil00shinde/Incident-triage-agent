from dataclasses import dataclass
from time import perf_counter

import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
from base import IncidentReport


client = OpenAI()


@dataclass(frozen=True)
class CallMetrics:
    latency_seconds: float
    input_tokens: int
    output_tokens: int
    total_tokens: int
    request_id: str | None


class IncidentAnalysisError(RuntimeError):
    pass 


SYSTEM_PROMPT = """
Analyze incidents using only the provided evidence. Do not invent facts.

Severity rubric:
- SEV1: Total production outage, confirmed serious security compromise,
  data loss, or critical functionality unavailable to most users.
- SEV2: Major production degradation or partial outage affecting many users.
- SEV3: Limited production impact, a small affected group, or a workaround exists.
- SEV4: Local/development/staging issue or minor issue with no user impact.
- UNKNOWN: The environment or impact evidence is insufficient.

Separate observed evidence from hypotheses. Hypotheses must include confidence.
"""


def analyze_incident(incident: str) -> tuple[IncidentReport, CallMetrics]:
    started_at = perf_counter()

    try:
        response = client.responses.parse(
            model="gpt-5.5",
            instructions=SYSTEM_PROMPT,
            input=incident,
            text_format=IncidentReport,
        )
    except openai.AuthenticationError as exc:
        raise IncidentAnalysisError(
            "Authentcation failed. Check OPENAI_API_KEY."
        ) from exc

    except openai.RateLimitError as exc:
        raise IncidentAnalysisError(
            "The API rate limit was reached."
        ) from exc 

    except openai.APITimeoutError as exc:
        raise IncidentAnalysisError(
            "Could not connect to the OpenAI API."
        ) from exc 

    except openai.APIError as exc:
        raise IncidentAnalysisError(
            "The OpenAI API request failed."
        ) from exc 


    if response.output_parsed  is None:
        raise IncidentAnalysisError(
            "The model returned no structered incident report."
        )

    usage = response.usage 

    metrics = CallMetrics(
        latency_seconds=perf_counter() - started_at,
        input_tokens=usage.input_tokens if usage else 0,
        output_tokens=usage.output_tokens if usage else 0,
        total_tokens=usage.total_tokens if usage else 0,
        request_id=getattr(response, "_request_id", None),
    )

    return response.output_parsed, metrics

    