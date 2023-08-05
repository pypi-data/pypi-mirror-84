python_code = """
import re

from sym import events, okta, pagerduty, rego, schedule, slack
from sym.annotations import hook, reducer

# @hook can yield a sym.event
# @reducer must return a single value (type depends on the reducer)
# @action implements a side-effect

# Available hooks: on_prompt, on_request, on_approval
# Available actions: after_prompt, after_request, after_approval
# Available reducers: get_approver


def modal_1(config):
    return {
        "type": "modal",
        "callback_id": "descriptor_callback",
        "title": {"type": "plain_text", "text": "Sym Request", "emoji": True},
        "submit": {"type": "plain_text", "text": "Next", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": ":wave: Hey jon! Please tell me more about this request.",
                    "emoji": True,
                },
            },
            {"type": "divider"},
            {
                "type": "input",
                "block_id": "descriptor_block",
                "label": {"type": "plain_text", "text": "Resource ID", "emoji": True},
                "element": {
                    "type": "radio_buttons",
                    "action_id": "descriptor",
                    "options": config.escalation_strategies,
                },
            },
        ],
    }


@hook
async def on_prompt(event):
    # This should be an event that fires instead of an await:
    resp = await slack.modals(modal_1, modal_2, [event])
    yield events.approval.request(resp)


@hook  # Hook name defaults to function name
def on_request(event):
    if pagerduty.on_call(event.user):
        # We will statically analyze this and validate this workflow exists
        schedule("tomorrow", "sym:incident_follow_up", event)
        yield events.approval.approved()

    if not rego.eval("./approval.rego", {"user": event.user}):
        yield events.approval.denied()


@reducer
def get_approver(request):
    if re.search(r"^arn:aws:s3", request.values["arn"]):
        return okta.group("data-security")
    return slack.channel("#ops")


@hook
def on_approval(event):
    if not event.approver.in_group(okta.group("ops")):
        yield events.approval.denied()
"""
