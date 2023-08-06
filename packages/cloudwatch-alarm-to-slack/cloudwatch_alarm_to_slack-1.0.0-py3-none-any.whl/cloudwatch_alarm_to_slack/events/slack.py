"""Module to send a cloudwatch alarm as a message to slack."""

import json
import os

from slack_sdk import WebClient

import cloudwatch_alarm_to_slack.templates.slack as SlackTemplates
import cloudwatch_alarm_to_slack.utils.log as log
from cloudwatch_alarm_to_slack.errors import EnvironmentVariableNotFound

LOGGER = log.custom_logger(__name__)


class Slack:
    """Handle interaction with slack."""
    def __init__(self):
        """Set environment variables."""
        if not os.getenv('SLACK_BOT_TOKEN'):
            raise EnvironmentVariableNotFound("SLACK_BOT_TOKEN not set.")

        if not os.getenv('SLACK_CHANNEL'):
            raise EnvironmentVariableNotFound("SLACK_CHANNEL not set.")

        self.slack_token = os.getenv('SLACK_BOT_TOKEN')
        self.slack_channel = os.getenv('SLACK_CHANNEL')

    def client(self):  # pragma: no cover
        """Create a slack client."""
        return WebClient(token=self.slack_token)

    def send_message(self, attachment=None):  # pragma: no cover
        """Sends message to slack."""
        LOGGER.info('Sending message to slack: %s', attachment)
        self.client().chat_postMessage(
            text='*AWS Cloudwatch Notification*',
            attachments=json.dumps(attachment),
            channel=self.slack_channel
        )

    @staticmethod
    def format_message(alarm=None, state=None):
        """Formats cloudwatch alarm details for slack."""
        return SlackTemplates.slack_attachment(
            alarm=alarm,
            state=state
        )
