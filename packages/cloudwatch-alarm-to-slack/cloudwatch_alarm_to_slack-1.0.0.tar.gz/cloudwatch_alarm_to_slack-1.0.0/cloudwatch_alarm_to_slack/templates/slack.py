"""Module to format slack message for a cloudwatch alarm event."""


def slack_attachment(alarm, state):
    """Return the slack attachment for a cloudwatch alarm."""
    return [
        {
            "color": state,
            "type": "mrkdwn",
            "fields": [
                {
                    "title": "Account",
                    "value": alarm.account,
                    "short": True
                },
                {
                    "title": "Region",
                    "value": alarm.region,
                    "short": True
                },
                {
                    "title": "Alarm Name",
                    "value": alarm.name,
                    "short": False
                },
                {
                    "title": "Alarm Description",
                    "value": alarm.description,
                    "short": False
                },
                {
                    "title": "Trigger",
                    "value": alarm.trigger.statistic + " of "
                    + alarm.trigger.metric + " "
                    + alarm.trigger.comparison_operator + " "
                    + str(alarm.trigger.threshold) + " for "
                    + str(alarm.trigger.evaluation_period) + " period(s) of "
                    + str(alarm.trigger.period) + " seconds.",
                    "short": False
                }
            ],
        }
    ]
