"""Test for cloudwatch_alarm_to_slack/templattes/slack."""

import pytest

from cloudwatch_alarm_to_slack.models.cloudwatch import CloudwatchEvent, CloudwatchTrigger
from cloudwatch_alarm_to_slack.templates.slack import slack_attachment


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
def test_slack_attachment_returns_valid_attachment(expected):
    """Test if slack_attachment returns a valid slack attachment for an alarm."""
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

    attachment = slack_attachment(cloudwatch_event, "danger")
    assert attachment == expected
