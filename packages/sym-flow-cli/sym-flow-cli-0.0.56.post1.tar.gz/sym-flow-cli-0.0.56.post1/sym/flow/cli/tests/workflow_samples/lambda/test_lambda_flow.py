from .lambda_flow import lambda_flow


class TestApproval:
    def testApprovalFlow(self):
        assert lambda_flow is not None
        assert lambda_flow.template is not None
        assert lambda_flow.template.version.major == 1
        assert lambda_flow.template.param_specs is not None
        assert len(lambda_flow.template.param_specs) == 1
        assert lambda_flow.params is not None
        assert len(lambda_flow.params) == 2

    def testLambdaParam(self):
        assert len(lambda_flow.params) == 2
        escalationParam = None
        for param in lambda_flow.params:
            if param.name == "escalation_strategies":
                escalationParam = param
                break

        assert escalationParam is not None
