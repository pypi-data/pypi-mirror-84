from sym.protos.tf.models import (
    Flow,
    Param,
    ParamSpec,
    Reducer,
    ReducerReturns,
    Source,
    Template,
    Version,
)

from .django import python_code

django_template = Template(
    name="sym:access:1.0",
    version=Version(major=1, minor=0),
    param_specs=[ParamSpec(name="org", required=True, default_value="widgets, inc")],
    reducers=[
        Reducer("get_reducer", required=True, returns=ReducerReturns(types=["string"]))
    ],
)

user_id_param = Param(name="user_id", type="string", required=True)

django_flow = Flow(
    name="django",
    version=Version(major=1, minor=0),
    template=django_template,
    implementation=Source("django.py", python_code),
    params=[user_id_param],
)
