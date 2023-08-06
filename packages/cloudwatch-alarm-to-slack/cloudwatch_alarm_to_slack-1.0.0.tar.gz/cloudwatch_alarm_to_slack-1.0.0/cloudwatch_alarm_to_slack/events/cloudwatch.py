"""Module to process incoming cloudwatch event for an alarm."""

import cloudwatch_alarm_to_slack.utils.log as log
from cloudwatch_alarm_to_slack.events.slack import Slack
from cloudwatch_alarm_to_slack.models.cloudwatch import (CloudwatchEvent,
                                                         CloudwatchTrigger)

LOGGER = log.custom_logger(__name__)


class CloudwatchAlarm:
    """Handle a cloudwatch alarm from SNS."""

    @staticmethod
    def process_alarm(alarm={}):
        """Process incoming cloudwatch alarm."""
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

        LOGGER.info(' Processing Cloudwatch event: %s', cloudwatch_event)
        alarm_state = CloudwatchAlarm.message_status(alarm_state=alarm.get('NewStateValue'))
        attachment = Slack.format_message(
            alarm=cloudwatch_event,
            state=alarm_state
        )
        Slack().send_message(
            attachment=attachment
        )

    @staticmethod
    def message_status(alarm_state=None):
        """Set status of slack message based on cloudwatch alarm status."""
        if alarm_state == "ALARM":
            color = "danger"
        elif alarm_state == "OK":
            color = "good"
        else:
            color = "warning"

        return color
