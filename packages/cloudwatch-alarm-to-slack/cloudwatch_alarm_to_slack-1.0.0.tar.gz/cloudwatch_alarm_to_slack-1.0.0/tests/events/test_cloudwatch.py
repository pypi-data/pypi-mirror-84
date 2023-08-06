"""Test for cloudwatch_alarm_to_slack/events/cloudwatch."""

import pytest

from unittest import mock

from cloudwatch_alarm_to_slack.events.cloudwatch import CloudwatchAlarm
from cloudwatch_alarm_to_slack.models.cloudwatch import CloudwatchEvent, CloudwatchTrigger


@pytest.mark.parametrize(
    "expected",
    [
        "danger"
    ]
)
def test_message_status_danger(expected):
    "Test if message_status returns danger(red) for cloudwatch alarm in alarm."
    color = CloudwatchAlarm.message_status(alarm_state="ALARM")
    assert color == expected


@pytest.mark.parametrize(
    "expected",
    [
        "good"
    ]
)
def test_message_status_good(expected):
    "Test if message_status returns good(green) for cloudwatch alarm that is resolved."
    color = CloudwatchAlarm.message_status(alarm_state="OK")
    assert color == expected


@pytest.mark.parametrize(
    "expected",
    [
        "warning"
    ]
)
def test_message_status_warning(expected):
    "Test if message_status returns warning(yellow) for cloudwatch alarm that has insufficient data."
    color = CloudwatchAlarm.message_status(alarm_state="INSUFFICIENT_DATA")
    assert color == expected


@mock.patch('cloudwatch_alarm_to_slack.events.cloudwatch.CloudwatchAlarm.message_status')
@mock.patch('cloudwatch_alarm_to_slack.events.cloudwatch.Slack.format_message')
@mock.patch('cloudwatch_alarm_to_slack.events.cloudwatch.Slack')
@mock.patch('cloudwatch_alarm_to_slack.events.slack.Slack.client')
def test_process_alarm(mock_slack, mock_slack_class, mock_slack_format_message, mock_cloudwatch_alarm_status):
    """Test if the cloudwatch alarm event is processed and a slack message is sent."""
    mock_alarm = {
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

    mock_cloudwatch_event = CloudwatchEvent(
            account=mock_alarm.get('AWSAccountId'),
            name=mock_alarm.get('AlarmName'),
            description=mock_alarm.get('AlarmDescription'),
            region=mock_alarm.get('Region'),
            state=mock_alarm.get('NewStateValue'),
            trigger=CloudwatchTrigger(
                metric=mock_alarm.get('Trigger').get('MetricName'),
                namespace=mock_alarm.get('Trigger').get('Namespace'),
                statistic=mock_alarm.get('Trigger').get('Statistic'),
                comparison_operator=mock_alarm.get('Trigger').get('ComparisonOperator'),
                threshold=mock_alarm.get('Trigger').get('Threshold'),
                period=mock_alarm.get('Trigger').get('Period'),
                evaluation_period=mock_alarm.get('Trigger').get('EvaluationPeriods')
            )
        )

    mock_slack_attachment = [
        {
            "color": "danger",
            "type": "mrkdwn",
            "fields": [
                {
                    "title": "Account",
                    "value": "test_account",
                    "short": True
                },
                {
                    "title": "Region",
                    "value": "US West (Oregon)",
                    "short": True
                },
                {
                    "title": "Alarm Name",
                    "value": "test_alarm",
                    "short": False
                },
                {
                    "title": "Alarm Description",
                    "value": "test_description",
                    "short": False
                },
                {
                    "title": "Trigger",
                    "value": "SUM" + " of "
                    + "Invocations" + " "
                    + "LessThanOrEqualToThreshold" + " "
                    + str(0.0) + " for "
                    + str(1) + " period(s) of "
                    + str(60) + " seconds.",
                    "short": False
                }
            ],
        }
    ]

    mock_slack_format_message.return_value = mock_slack_attachment
    mock_cloudwatch_alarm_status.return_value = "ALARM"
    slack = mock_slack_class.return_value

    CloudwatchAlarm.process_alarm(alarm=mock_alarm)
    mock_cloudwatch_alarm_status.assert_called_once_with(alarm_state="ALARM")
    mock_slack_format_message.assert_called_once_with(
        alarm=mock_cloudwatch_event,
        state="ALARM"
    )
    slack.send_message.assert_called_once_with(attachment=mock_slack_attachment)
