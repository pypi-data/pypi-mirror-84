python_code = """
from sym.annotations import hook, reducer
from sym.channels import slack
from sym.events import approval as events
from sym.integrations import pagerduty

# This is the use case for SaasWorks.
# https://docs.google.com/document/d/1mzheWIZSGwC3BtjtlneKprMS_Och0M2NT-NwQKPjdMI/edit


def is_off_hours():
    # check if it's nighttime
    ...


@reducer
def get_approver(event):
    if event.resource.name == "sensitive_db":
        return slack.group([slack.user("jim"), slack.user("matt")])  # Group DM


@hook
def on_request(event):
    # the schedule name refers to a named integration that
    # has been set up in the Sym UI, along with a pagerduty API key
    if is_off_hours() and pagerduty.on_call(
        event.user, schedule='eng-on-call-rotation'
    ):
        return events.approve()
"""
