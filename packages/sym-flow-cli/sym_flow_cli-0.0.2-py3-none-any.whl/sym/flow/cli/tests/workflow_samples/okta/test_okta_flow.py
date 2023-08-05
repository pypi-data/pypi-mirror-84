import pytest

from .okta_flow import escalationParam, okta_flow


class TestApproval:
    def testApprovalFlow(self):
        assert okta_flow is not None
        assert okta_flow.template is not None

    def testLambdaParam(self):
        assert len(okta_flow.params) == 1
        escalationParam = None
        for param in okta_flow.params:
            if param.name == "escalation_strategies":
                escalationParam = param
                break

        assert escalationParam is not None
