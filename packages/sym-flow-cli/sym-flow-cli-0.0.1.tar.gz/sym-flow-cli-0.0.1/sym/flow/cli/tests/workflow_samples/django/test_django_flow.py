from .django_flow import django_flow


class TestApproval:
    def testApprovalFlow(self):
        assert django_flow is not None
        assert django_flow.template is not None
        assert django_flow.template.version.major == 1
        assert django_flow.template.param_specs is not None
        assert len(django_flow.template.param_specs) == 1
        assert django_flow.params is not None
        assert len(django_flow.params) == 1

    def testRequestParam(self):
        userIDParam = None
        for param in django_flow.params:
            if param.name == "user_id":
                userIDParam = param
                break

        assert userIDParam is not None
        assert userIDParam.value is None or userIDParam.value.value_type == ""
        assert userIDParam.type == "string"
