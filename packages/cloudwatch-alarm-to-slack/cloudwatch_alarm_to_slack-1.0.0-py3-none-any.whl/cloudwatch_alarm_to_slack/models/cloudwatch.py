"""Module to define the data model for cloudwatch event and trigger."""

from pydantic.dataclasses import dataclass


@dataclass
class CloudwatchTrigger:
    """Model for a Cloudwatch event."""
    metric: str
    namespace: str
    statistic: str
    comparison_operator: str
    threshold: int
    period: int
    evaluation_period: int


@dataclass
class CloudwatchEvent:
    """Model for a Cloudwatch trigger."""
    account: str
    name: str
    description: str
    region: str
    state: str
    trigger: CloudwatchTrigger
