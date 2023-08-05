python_code = """
from sym.annotations import reducer
from sym.channels import slack

# This is the use case for the Split integration.
# Similar to Django, but hits the Split API.


@reducer
def get_approver(event):
    return slack.channel(event.user.config["partnerships"]["split"]["slack_channel"])
"""
