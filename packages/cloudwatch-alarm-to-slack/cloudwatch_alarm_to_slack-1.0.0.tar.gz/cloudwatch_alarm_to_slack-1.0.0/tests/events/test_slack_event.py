"""Test for cloudwatch_alarm_to_slack/events/slack."""

import pytest

from cloudwatch_alarm_to_slack.models.cloudwatch import CloudwatchEvent, CloudwatchTrigger
from cloudwatch_alarm_to_slack.events.slack import Slack
from cloudwatch_alarm_to_slack.errors import EnvironmentVariableNotFound


@pytest.mark.parametrize(
    "expected",
    [
        [
            {
                "color": "danger",
                "type": "mrkdwn",
                "fields": [
                    {
                        "short": True,
                        "title": "Account",
                        "value": "test_account"
                    },
                    {
                        "short": True,
                        "title": "Region",
                        "value": "US West (Oregon)"
                    },
                    {
                        "short": False,
                        "title": "Alarm Name",
                        "value": "test_alarm"
                    },
                    {
                        "short": False,
                        "title": "Alarm Description",
                        "value": "test_description"
                    },
                    {
                        "short": False,
                        "title": "Trigger",
                        "value": "SUM of Invocations LessThanOrEqualToThreshold 0 for 1 "
                                 "period(s) of 60 seconds."
                    }
                ],
            }
        ]
    ]
)
def test_slack_format_message_receives_valid_slack_attachment(expected):
    """Test if format_message receives a valid slack attachment for an alarm."""
    alarm = {
        'AlarmName': 'test_alarm',
        'AlarmDescription': 'test_description',
        'AWSAccountId': 'test_account',
        'NewStateValue': 'ALARM',
        'Region': 'US West (Oregon)',
        'OldStateValue': 'INSUFFICIENT_DATA',
        'Trigger': {
            'MetricName': 'Invocations',
            'Namespace': 'test_service',
            'StatisticType': 'Statistic',
            'Statistic': 'SUM',
            'Period': 60,
            'EvaluationPeriods': 1,
            'ComparisonOperator': 'LessThanOrEqualToThreshold',
            'Threshold': 0.0
        }
    }
    cloudwatch_event = CloudwatchEvent(
            account=alarm.get('AWSAccountId'),
            name=alarm.get('AlarmName'),
            description=alarm.get('AlarmDescription'),
            region=alarm.get('Region'),
            state=alarm.get('NewStateValue'),
            trigger=CloudwatchTrigger(
                metric=alarm.get('Trigger').get('MetricName'),
                namespace=alarm.get('Trigger').get('Namespace'),
                statistic=alarm.get('Trigger').get('Statistic'),
                comparison_operator=alarm.get('Trigger').get('ComparisonOperator'),
                threshold=alarm.get('Trigger').get('Threshold'),
                period=alarm.get('Trigger').get('Period'),
                evaluation_period=alarm.get('Trigger').get('EvaluationPeriods')
            )
        )

    attachment = Slack.format_message(cloudwatch_event, "danger")
    assert attachment == expected


def test_bot_token_not_found_user_exception(monkeypatch):
    """Test if EnvironmentVariableNotFound is raised when SLACK_BOT_TOKEN is not set."""
    monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)

    with pytest.raises(EnvironmentVariableNotFound):
        Slack()


def test_slack_channel_not_found_user_exception(monkeypatch):
    """Test if EnvironmentVariableNotFound is raised when SLACK_CHANNEL is not set."""
    monkeypatch.delenv("SLACK_CHANNEL", raising=False)

    with pytest.raises(EnvironmentVariableNotFound):
        Slack()
