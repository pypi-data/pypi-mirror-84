from sym.protos.tf.models import (
    CompositeValue,
    CompositeValueField,
    EscalationStrategy,
    Flow,
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

from .okta import python_code

okta_template = Template(
    name="sym:access:1.0",
    version=Version(major=1, minor=0),
    param_specs=[ParamSpec(name="org", required=True, default_value="foobar")],
    reducers=[
        Reducer("get_approver", required=True, returns=ReducerReturns(types=["string"]))
    ],
)

escalation_strategies = CompositeValue(
    name="escalation_strategies",
    fields=[
        CompositeValueField(
            name="okta_prod",
            type="okta_strategy",
            escalation_strategy=EscalationStrategy(
                name="okta_prod",
                required=False,
                type="okta",
                okta=OktaStrategy(
                    id="okta-prod",
                    org_name="dev-123456",
                    client_id="0ob52x31c8bIswyu24c9",
                    private_key="data.vault_generic_secret.sym_okta_key",
                    allowed_values=["OktaGroupOne", "OktaGroupTwo"],
                ),
            ),
        ),
        CompositeValueField(
            name="okta-staging",
            type="okta_strategy",
            escalation_strategy=EscalationStrategy(
                name="okta-staging",
                required=False,
                type="okta",
                okta=OktaStrategy(
                    id="okta-staging",
                    label="Okta-Prod",
                ),
            ),
        ),
    ],
)


escalationParam = Param(
    name="escalation_strategies", value=SymValue(composite_value=escalation_strategies)
)

okta_flow = Flow(
    name="okta",
    version=Version(major=1, minor=0),
    template=okta_template,
    implementation=Source("okta.py", python_code),
    params=[escalationParam],
)
