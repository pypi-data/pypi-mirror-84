python_code = """"
from sym.annotations import reducer
from sym.channels import slack
from sym.integrations import okta

# This is the Courier use case.


# class Okta:
#   def group_match(self, mapping, user):
#       groups = user.identities['okta'].groups
#       for group, value in mapping.items():
#           if group in groups:
#               return value


@reducer
def get_approver(event):
    group_to_channels = {
        'eng': '#eng',
        'ops': '#operations',
        'customer-success': '#operations',
    }
    channel = okta.group_match(group_to_channels, user=event.user)
    return slack.channel(channel)
"""
