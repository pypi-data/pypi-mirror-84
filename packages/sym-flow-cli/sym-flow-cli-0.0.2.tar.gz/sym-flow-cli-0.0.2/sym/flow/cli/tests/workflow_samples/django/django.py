python_code = """
from sym.annotations import reducer
from sym.channels import slack

# This is the Klaviyo use case


@reducer
def get_approver(event):
    return slack.channel("#impersonations")
"""
