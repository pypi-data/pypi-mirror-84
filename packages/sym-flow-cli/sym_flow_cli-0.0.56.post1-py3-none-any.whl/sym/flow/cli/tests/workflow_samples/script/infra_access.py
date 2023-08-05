python_code = """
from sym.annotations import hook, action, reducer
from sym import slack, pagerduty, events, schedule

# @hook _can_ return a sym.event
# @reducer _must_ return a single value (type depends on the reducer)
# @action implements a side-effect

# Available hooks: on_prompt, on_request, on_approval
# Available actions: after_prompt, after_request, after_approval
# Available reducers: get_approver

# Runtime:

def fn(evt, ctx, impl):
    name = ctx.handler.name
    if impl.hook[name]:
        try:
            for new_evt in impl.hook[name]():
                ctx.append(new_evt)
                # send_to_api(new_evt)
        except StopIteration as e:
            send_to_api(e.event)
            return
    ctx.handler()
    if impl.actions[name]:
        impl.actions[name]()


@reducer
def get_approver(event):
    if event.resource.type == "s3":
        return slack.channel("#ops")


@hook
def on_request(event):
    if pagerduty.on_call(event.user):
        yield schedule("tomorrow", "sym:incident_follow_up:1.0", event)
        return events.approval.approve()
"""
