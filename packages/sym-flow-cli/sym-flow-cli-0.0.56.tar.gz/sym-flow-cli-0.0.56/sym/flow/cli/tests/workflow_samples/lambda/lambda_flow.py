from sym.protos.tf.models import (
    AtomicValue,
    CompositeValue,
    CompositeValueField,
    EscalationStrategy,
    Flow,
    LabeledValue,
    LambdaStrategy,
    Param,
    ParamSpec,
    Reducer,
    ReducerReturns,
    Source,
    SymValue,
    Template,
    Version,
)

from .lambda_code import python_code

lambda_template = Template(
    name="sym:access:1.0",
    version=Version(major=1, minor=0),
    param_specs=[ParamSpec(name="org", required=True, default_value="widgets, inc")],
    reducers=[
        Reducer("get_reducer", required=True, returns=ReducerReturns(types=["string"]))
    ],
)

org_param = Param(
    name="org",
    type="string",
    value=SymValue(atomic_value=AtomicValue(string_value="Healthy Health")),
)

escalation_strategies = CompositeValue(
    name="escalation_strategies",
    fields=[
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
        )
    ],
)

escalation_param = Param(
    name="escalation_strategies", value=SymValue(composite_value=escalation_strategies)
)


lambda_flow = Flow(
    name="lambda",
    version=Version(major=1, minor=0),
    template=lambda_template,
    implementation=Source("lambda_code.py", python_code),
    params=[escalation_param, org_param],
)
