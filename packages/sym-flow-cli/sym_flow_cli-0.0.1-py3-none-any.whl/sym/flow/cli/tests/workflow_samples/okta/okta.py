python_code = """
from sym.annotations import reducer
from sym.channels import slack

# This is the LD use case.


@reducer
def get_approver(event):
    return slack.channel(
        event.request.channel
    )  # whatever channel the request was made in
"""
