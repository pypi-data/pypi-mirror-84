from sym.protos.tf.models import (
    AwsStrategy,
    CompositeFieldSpecField,
    CompositeValue,
    CompositeValueField,
    EscalationStrategy,
    FieldSpec,
    Flow,
    LabeledValue,
    LambdaStrategy,
    OktaStrategy,
    Param,
    ParamSpec,
    Reducer,
    ReducerReturns,
    Source,
    SymValue,
    Template,
    Version,
)

from .approval import python_code

approval_template = Template(
    name="sym:approval:1.0",
    version=Version(major=1, minor=0),
    param_specs=[ParamSpec(name="org", required=True, default_value="foobar")],
    reducers=[
        Reducer("get_approver", required=True, returns=ReducerReturns(types=["string"]))
    ],
)

requestData = CompositeValue(
    fields=[
        CompositeValueField(
            type="field", field_value=FieldSpec(name="reason", required=True, type="str")
        ),
        CompositeFieldSpecField(
            type="field",
            field_spec=FieldSpec(
                name="arn",
                required=True,
                type="str",
                label="ARN of resource you don't have access to",
            ),
        ),
        CompositeFieldSpecField(
            type="field",
            field_spec=FieldSpec(
                name="fave_color", required=False, type="str", label="Favorite Color"
            ),
        ),
    ]
)

escalation_strategies = CompositeValue(
    name="escalation_strategies",
    fields=[
        CompositeValueField(
            name="aws_strategy",
            type="aws_strategy",
            escalation_strategy=EscalationStrategy(
                name="aws_strategy",
                required=True,
                type="aws",
                aws=AwsStrategy(
                    id="aws-prod",
                    label="AWS-Prod",
                    allowed_values=["AWSGroupOne", "AWSGroupTwo"],
                    role_arn="arn:aws:iam::123456789012:role/sym/SymExecute-aws-prod",
                ),
            ),
        ),
        CompositeValueField(
            name="okta_strategy",
            type="okta_strategy",
            escalation_strategy=EscalationStrategy(
                name="okta_strategy",
                required=True,
                type="okta",
                okta=OktaStrategy(
                    id="okta-prod",
                    label="Okta-Prod",
                    org_name="dev-123456",
                    client_id="0ob52x31c8bIswyu24c9",
                    private_key="data.vault_generic_secret.sym_okta_key",
                    allowed_values=["OktaGroupOne", "OktaGroupTwo"],
                ),
            ),
        ),
        CompositeValueField(
            name="lambda_strategy",
            type="lambda_strategy",
            escalation_strategy=EscalationStrategy(
                name="my lambda",
                required=True,
                type="lambda",
                okta=LambdaStrategy(
                    id="okta-prod",
                    label="Okta-Prod",
                    approval_function_name="my-lambda-approval",
                    expiration_function_name="my-lambda-expiration",
                    role_arn="arn:aws:iam::123456789012:role/sym/SymExecute-my-lambda",
                    allowed_values=[
                        LabeledValue("Label 1", "value1"),
                        LabeledValue("Label 2", "value2"),
                    ],
                ),
            ),
        ),
    ],
)

requestParam = Param(
    name="escalation_strategies", value=SymValue(composite_value=requestData)
)

escalationParam = Param(
    name="request_fields", value=SymValue(composite_value=escalation_strategies)
)

approval_flow = Flow(
    name="infra_access_flow",
    version=Version(major=1, minor=0),
    template=approval_template,
    implementation=Source("approval.py", python_code),
    params=[escalationParam, requestParam],
)
