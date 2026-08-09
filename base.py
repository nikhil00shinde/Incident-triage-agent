from typing import Literal

from pydantic import BaseModel


class Hypothesis(BaseModel):
    cause: str
    supporting_evidence: list[str]
    confidence: Literal["low","medium","high"]


class IncidentReport(BaseModel):
    severity: Literal["SEV1", "SEV2", "SEV3","SEV4", "UNKNOWN"]
    summary: str
    observed_evidence: list[str]
    hypotheses: list[Hypothesis]
    immediate_actions: list[str]
    missing_information: list[str]


