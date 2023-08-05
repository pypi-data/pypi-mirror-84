from .approval_flow import approval_flow


class TestApproval:
    def testApprovalFlow(self):
        assert approval_flow is not None
        assert approval_flow.template is not None
        assert approval_flow.template.version.major == 1
        assert approval_flow.template.param_specs is not None
        assert len(approval_flow.template.param_specs) == 1
        assert approval_flow.params is not None
        assert len(approval_flow.params) == 2

    def testEscalationParam(self):
        escalationParam = None
        for param in approval_flow.params:
            if param.name == "escalation_strategies":
                escalationParam = param
                break

        assert escalationParam is not None
        assert escalationParam.value is not None
        assert escalationParam.value.composite_value is not None

        fields = escalationParam.value.composite_value.fields
        assert fields is not None
        assert len(fields) == 3
